import tkinter as tk
from tkinter import ttk
import json
from tkinter import filedialog
from espmega_lightshow.drivers import UniversalLightGrid, LightDriver, ESPMegaLightDriver, HomeAssistantLightDriver
from dataclasses import dataclass
import sys
import json
import sys
from tkinter import messagebox
import tkinter.messagebox as messagebox
import os
from time import sleep, perf_counter
import time
import statistics
from importlib import util as importlib_util
from espmega_lightshow.scripting import UserScript
import shutil
import traceback
import webbrowser
import subprocess
import re
from PIL import Image, ImageTk

# Constants Definitions
LIGHT_DISABLED = -1
LIGHT_OFF = 0
LIGHT_ON = 1
COLOR_ON = "white"
COLOR_OFF = "gray"
COLOR_DISABLED = "gray12"
COLOR_OFF_OFFLINE = "brown4"
COLOR_ON_OFFLINE = "red"
MIN_BPM = 20
MAX_BPM = 600
CONFIG_FILE = "config.json"

# Choose the light grid class to use
# The UniversalLightGrid class is recommended
LightGrid = UniversalLightGrid

# Messagebox Constants
MSG_LOAD_ERROR_TITLE = "Load Error"
MSG_FILE_NOT_FOUND_TITLE = "The file could not be found."
MSG_SCRIPT_ERROR_TITLE = "Script Error"

# File Dialog Constants
FILE_TYPE_JSON = ("JSON Files", "*.json")
FILE_TYPE_PYTHON = ("Python Files", "*.py")

# Playback Status Constants
PLAYBACK_STATUS_STOPPED = "Status: Stopped"
PLAYBACK_STATUS_PLAYING = "Status: Playing"
PLAYBACK_STATUS_SCRIPTED = "Status: Scripted"

# Window Constants
WINDOW_TITLE = "ESPMega Light Show"

def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)


global light_server
global light_server_port
global rapid_mode
global light_map_file
global light_grid
global design_mode
global animation_quick_load_slots
global script_quick_load_slots
global script_active
global configured

animation_quick_load_slots = [None]*5
script_quick_load_slots = [None]*5
script_active = False

light_map_file = ""  # Default light map file

# Get Icon File Path
icon_image = Image.open(os.path.join(os.path.dirname(__file__), "logo.png"))
icon_image = icon_image.resize((32, 32))

# Get Logo File Path
logo_file = os.path.join(os.path.dirname(__file__), "logo.png")

# Load config.json if it exists
try:
    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)
    light_server = config["light_server"]
    light_server_port = config["light_server_port"]
    rapid_mode = config["rapid_mode"]
    light_map_file = config["light_map_file"]
    design_mode = config["design_mode"]
    animation_quick_load_slots = config["animation_quick_load_slots"]
    script_quick_load_slots = config["script_quick_load_slots"]
except FileNotFoundError:
    light_server = ""
    light_server_port = 1883
    rapid_mode = False
    light_map_file = ""
    design_mode = False
except KeyError:
    # Delete the config file if it is corrupted
    os.remove(CONFIG_FILE)
    light_server = ""
    light_server_port = 1883
    rapid_mode = False
    light_map_file = ""
    design_mode = False
    # Inform the user that the config file is corrupted and that it has been deleted
    messagebox.showerror(
        "Error", "The config file is corrupted and has been deleted. Please reconfigure the program.")

# Check quick load slots integrity
if len(animation_quick_load_slots) != 5:
    messagebox.showerror(
        "Error", "The animation quick load slots are corrupted and have been reset.")
    animation_quick_load_slots = [None]*5
if len(script_quick_load_slots) != 5:
    messagebox.showerror(
        "Error", "The script quick load slots are corrupted and have been reset.")
    script_quick_load_slots = [None]*5

# Create a tkinter gui window ask for the light server ip and port and whether to enable rapid response mode
root = tk.Tk()
root.title("ELS Pre-Flight")
icon = ImageTk.PhotoImage(icon_image)
root.wm_iconphoto(True, icon)
root.geometry("600x360")
root.resizable(False, False)

configured = False

def submit_config():
    global light_server
    global light_server_port
    global rapid_mode
    global design_mode
    global configured
    light_server = light_server_entry.get()
    light_server_port = int(light_server_port_entry.get())
    rapid_mode = rapid_mode_var.get()
    design_mode = design_mode_var.get()
    if light_server == "":
        messagebox.showerror("Error", "Please enter the light server ip.")
        return
    if light_server_port == "":
        messagebox.showerror("Error", "Please enter the light server port.")
        return
    if light_map_file == "":
        messagebox.showerror("Error", "Please select a light map file.")
        return
    # Save the config to CONFIG_FILE
    with open(CONFIG_FILE, "w") as file:
        json.dump({"light_server": light_server, "light_server_port": light_server_port,
                  "rapid_mode": rapid_mode, "light_map_file": light_map_file, "design_mode": design_mode,
                  "script_quick_load_slots": script_quick_load_slots, "animation_quick_load_slots": animation_quick_load_slots}, file)
    configured = True
    root.destroy()


def open_light_map_file_chooser_dialog():
    global light_map_file
    light_map_file = filedialog.askopenfilename(
        filetypes=[FILE_TYPE_JSON])
    light_map_button.config(text=light_map_file)

# Create a label for the title
title_label = ttk.Label(root, text="ESPMega Lightshow Setup", font=("Arial", 24))
title_label.pack()

# Create a small label to explain design mode
design_mode_label = ttk.Label(
    root, text="Design mode allows you to play with the lights without connecting to a controller.\nThis is useful for testing lighting designs.")
design_mode_label.pack()

# Create a design mode toggle
design_mode_var = tk.BooleanVar()
design_mode_toggle = ttk.Checkbutton(
    root, text="Design Mode", variable=design_mode_var)
design_mode_toggle.pack()

# Create a field to enter the light server ip
light_server_label = ttk.Label(root, text="Light Server IP")
light_server_label.pack()
light_server_entry = ttk.Entry(root)
light_server_entry.pack()

# Create a field to enter the light server port
light_server_port_label = ttk.Label(root, text="Light Server Port")
light_server_port_label.pack()
light_server_port_entry = ttk.Entry(root)
light_server_port_entry.pack()

# Create a small label to explain rapid response mode
rapid_response_label = ttk.Label(
    root, text="Rapid response mode makes the lights respond faster by disabling the acknowledgement from the controller.\nThis is useful if multiple lights are being controlled at once and are on the same controller.")
rapid_response_label.pack()

# Create a checkbox to enable rapid response mode
rapid_mode_var = tk.BooleanVar()
rapid_mode_toggle = ttk.Checkbutton(
    root, text="Rapid Response Mode", variable=rapid_mode_var)
rapid_mode_toggle.pack()

# Create a text label for the light map file chooser
light_map_label = ttk.Label(root, text="Light Map File")
light_map_label.pack()

# Create a button to open a file dialog asking to select the light map file
light_map_button = ttk.Button(root, text="Browse..."if light_map_file ==
                             "" else light_map_file, command=open_light_map_file_chooser_dialog)
light_map_button.pack(pady=5)

# Create a button to submit the configuration and close the window
submit_button = ttk.Button(root, text="Submit", command=submit_config)
submit_button.pack(pady=5)


def open_generate_light_map_template_window():
    light_map_generator_window = tk.Toplevel(root)
    light_map_generator_window.title("Generate Map")
    icon = ImageTk.PhotoImage(icon_image)
    light_map_generator_window.wm_iconphoto(True, icon)
    light_map_generator_window.geometry("250x130")
    light_map_generator_window.resizable(False, False)

    # Create a field to enter the number of rows
    light_map_rows_label = ttk.Label(
        light_map_generator_window, text="Number of Rows")
    light_map_rows_label.pack()
    light_map_rows_entry = ttk.Entry(light_map_generator_window)
    light_map_rows_entry.pack()

    # Create a field to enter the number of columns
    light_map_columns_label = ttk.Label(
        light_map_generator_window, text="Number of Columns")
    light_map_columns_label.pack()
    light_map_columns_entry = ttk.Entry(light_map_generator_window)
    light_map_columns_entry.pack()

    def submit_light_map_template():
        rows = int(light_map_rows_entry.get())
        columns = int(light_map_columns_entry.get())
        light_map = [[None]*columns]*rows
        # Ask the user where to save the light map template
        filename = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[FILE_TYPE_JSON])
        with open(filename, "w") as file:
            json.dump(light_map, file)
        light_map_generator_window.destroy()

    # Create a button to submit the configuration and close the window
    submit_button = ttk.Button(light_map_generator_window,
                              text="Generate", command=submit_light_map_template)
    submit_button.pack(pady=5)


# Create a button to generate a template light map file with the specified dimensions with all lights disabled
light_map_generate_button = ttk.Button(
    root, text="Generate Light Map Template", command=open_generate_light_map_template_window)
light_map_generate_button.pack(pady=5)

# Fill in the default values
light_server_entry.insert(0, light_server)
light_server_port_entry.insert(0, light_server_port)
rapid_mode_var.set(rapid_mode)
design_mode_var.set(design_mode)

# Start the tkinter main loop
root.mainloop()

# Exit the program if the user closes the window
if not configured:
    sys.exit(0)

def state_to_color(state: int):
    if state == LIGHT_ON:
        return COLOR_ON
    elif state == LIGHT_OFF:
        return COLOR_OFF
    else:
        return COLOR_DISABLED


def color_to_state(color: str):
    if color == COLOR_ON:
        return LIGHT_ON
    elif color == COLOR_OFF:
        return LIGHT_OFF
    else:
        return LIGHT_DISABLED


# Load light map from light_map.json
light_grid = LightGrid(design_mode=design_mode)
light_grid.read_light_map_from_file(filename=light_map_file)
rows = light_grid.rows
columns = light_grid.columns

global playback_active
global current_frame
current_frame = 0
playback_active: bool = False

# -1 if light is disabled, 0 if light is offline, 1 if light is online

def check_light_online(row: int, column: int):
    if (light_grid.light_map[row][column] == None):
        return -1
    if (light_grid.get_physical_light(row, column) == None):
        return 0
    return 1

def set_tile_state(row: int, column: int, state: bool):
    # Get the tile element
    element = lightgrid_frame.grid_slaves(row=row, column=column)[0]
    # If the light is disabled, set the tile color to disabled
    if not light_grid.is_installed(row=row, column=column):
        element.config(bg=COLOR_DISABLED)
        return
    # Get Physical Light
    light = light_grid.get_physical_light(row, column)
    # Set the light state
    light.set_light_state(state)
    light_state = light_grid.get_light_state(row, column)
    print(f"Setting tile color at {row}, {column} to {light_state}")
    # Set the tile color
    if light_state == LightDriver.LIGHT_STATE_OFF:
        element.config(bg=COLOR_OFF)
    elif light_state == LightDriver.LIGHT_STATE_ON:
        element.config(bg=COLOR_ON)
    elif light_state == LightDriver.LIGHT_STATE_OFF_UNCONTROLLED:
        element.config(bg=COLOR_OFF_OFFLINE)
    elif light_state == LightDriver.LIGHT_STATE_ON_UNCONTROLLED:
        element.config(bg=COLOR_ON_OFFLINE)

def get_tile_state(row: int, column: int):
    # If the light is disabled, return disabled
    if not light_grid.is_installed(row=row, column=column):
        return LIGHT_DISABLED
    light = light_grid.get_physical_light(row, column)
    state = light.get_light_state()
    if state == LightDriver.LIGHT_STATE_ON or state == LightDriver.LIGHT_STATE_ON_UNCONTROLLED:
        return True
    elif state == LightDriver.LIGHT_STATE_OFF or state == LightDriver.LIGHT_STATE_OFF_UNCONTROLLED:
        return False


def change_color(event):
    global script_active
    global playback_active
    if script_active or playback_active:
        return
    row = event.widget.grid_info()["row"]
    column = event.widget.grid_info()["column"]
    set_tile_state(row, column, not get_tile_state(row, column))


def add_frame():
    frame = []
    for i in range(rows):
        row = []
        for j in range(columns):
            element_state = get_tile_state(i, j)
            row.append(element_state)
        frame.append(row)
    frames.append(frame)
    slider.config(to=len(frames)-1)  # Update the slider range
    slider.set(len(frames)-1)  # Set the slider value to the last frame
    # Update the slider position
    root.update()


def record_frame():
    frame_index = slider.get()
    frame = []
    for i in range(rows):
        row = []
        for j in range(columns):
            element_state = get_tile_state(i, j)
            row.append(element_state)
        frame.append(row)
    frames[frame_index] = frame
    render_frame_at_index(frame_index)
    # Update the slider position
    root.update()


def delete_frame():
    # Don't delete the last frame
    if len(frames) == 1:
        return
    frame_index = slider.get()
    frames.pop(frame_index)
    slider.config(to=len(frames)-1)  # Update the slider range
    if frame_index > 0:
        slider.set(frame_index-1)
        render_frame_at_index(frame_index-1)
    else:
        slider.set(0)
        render_frame_at_index(0)
    # Update the slider position
    root.update()


def save_animation():
    filename = filedialog.asksaveasfilename(
        defaultextension=".json", filetypes=[FILE_TYPE_JSON])
    if filename:
        with open(filename, "w") as file:
            json.dump(frames, file)


def move_frame_left():
    frame_index = slider.get()
    if frame_index > 0:
        frames[frame_index], frames[frame_index -
                                    1] = frames[frame_index-1], frames[frame_index]
        slider.set(frame_index-1)
        render_frame_at_index(frame_index-1)
    root.update()


def move_frame_right():
    frame_index = slider.get()
    if frame_index < len(frames)-1:
        frames[frame_index], frames[frame_index +
                                    1] = frames[frame_index+1], frames[frame_index]
        slider.set(frame_index+1)
        render_frame_at_index(frame_index+1)
    root.update()


def play_frames():
    global animation_id  # Declare animation_id as a global variable
    global playback_active
    global current_frame
    playback_active = True
    current_frame = slider.get()
    # If the current frame is the last frame and repeat is disabled, don't play
    if current_frame == len(frames)-1 and not repeat_var.get():
        playback_active = False
        return
    playback_status_label.config(text=PLAYBACK_STATUS_PLAYING)
    start_time = perf_counter()
    while current_frame < len(frames):
        if not playback_active:
            break
        render_frame_at_index(current_frame)
        slider.set(current_frame)  # Update the slider position
        speed = speed_scale.get()  # Get the value of the speed scale
        # Calculate the delay between frames in milliseconds based on speed
        delay = int(60000 / speed)
        root.update()
        # Delay between frames (in seconds)
        should_increment = True
        while perf_counter() - start_time < delay/1000:
            if not playback_active:
                break
            if speed_scale.get() != speed:
                should_increment = False
                break
            if slider.get() != current_frame:
                should_increment = False
                break
            root.update()
            root.update_idletasks()
        if should_increment:
            current_frame = slider.get()
            current_frame += 1
        else:
            current_frame = slider.get()
        start_time = perf_counter()
    repeat = repeat_var.get()  # Get the value of the repeat toggle
    if (repeat and playback_active):
        current_frame = 0
        slider.set(current_frame)
        play_frames()
    else:
        playback_status_label.config(text=PLAYBACK_STATUS_STOPPED)



def pause_frames():
    global playback_active
    playback_active = False


def stop_frames():
    global playback_active
    playback_active = False
    slider.set(0)
    render_frame_at_index(0)
    root.after_cancel(animation_id)


def scrub_frames(value):
    frame_index = int(value)
    render_frame_at_index(frame_index)
    root.update()


def render_frame(frame: list):
    for i in range(rows):
        for j in range(columns):
            set_tile_state(i, j, frame[i][j])


def change_light_config(event):
    # Get a list of all configuration options for each light driver
    config_options = {"disabled":[],"espmega": ESPMegaLightDriver.get_driver_properties()["configuration_parameters"], "homeassistant": HomeAssistantLightDriver.get_driver_properties()["configuration_parameters"]}
    config_vars = {}
    config_frames = {}
    global script_active
    global playback_active
    if script_active or playback_active:
        return
    row = event.widget.grid_info()["row"]
    column = event.widget.grid_info()["column"]
    light_config_window = tk.Toplevel(root)
    light_config_window.geometry("250x190")
    light_config_window.title("Light Config")
    icon = ImageTk.PhotoImage(icon_image)
    light_config_window.wm_iconphoto(True, icon)
    light_config_window.resizable(False, False)

    def submit_light_config():
        global light_grid
        
        physical_light_config = {}
        driver = light_driver_var.get()
        for config_var in config_vars[driver]:
            physical_light_config[config_var] = config_vars[driver][config_var].get()
        physical_light_config["driver"] = driver

        # Make sure that all the required config options are filled in
        for config_option in config_options[driver]:
            if config_option == "driver":
                continue
            if physical_light_config[config_option] == "":
                messagebox.showerror(
                    "Error", f"Please fill in the {config_option} field.")
                return

        # If the light is disabled, set the light config to None
        if driver == "disabled":
            physical_light_config = None

        # Update the light map
        modified_light_map = light_grid.light_map
        modified_light_map[row][column] = physical_light_config

        # Save the light map to the file
        with open(light_map_file, "w") as file:
            json.dump(light_grid.light_map, file)

        # Reload the light_grid
        light_grid = LightGrid(design_mode=design_mode)
        light_grid.read_light_map_from_file(filename=light_map_file)

        render_frame_at_index(slider.get())
        root.update()

        # Close the window
        light_config_window.destroy()

    def get_driver_from_json():
        # If the light is disabled, return disabled
        if light_grid.light_map[row][column] == None:
            return "disabled"
        return light_grid.light_map[row][column]["driver"]

    def load_config_to_entry_fields(driver):
        # Is the driver different from the driver in the json file?
        if driver != get_driver_from_json():
            # If so, clear all the entry fields instead of loading the config
            print("Driver is different, clearing entry fields")
            for config_var in config_vars[driver]:
                config_vars[driver][config_var].set("")
            root.update()
            return
        print("Driver is the same, loading config")
        # Load the light config that corresponds to the driver in the json file
        light_config = light_grid.light_map[row][column]
        # Load the config to the entry fields
        for config_var in config_vars[driver]:
            # Skip the driver config variable
            if config_var == "driver":
                continue
            print(f"Loading {config_var} to entry field, the value is {light_config[config_var]}")
            print(f"The entry field is {config_vars[driver][config_var]}")
            config_vars[driver][config_var].set(
                light_config[config_var])
            root.update()
    
    def resize_window():
        # Get Number of Config Options
        driver = light_driver_var.get()
        num_config_options = len(config_options[driver])
        light_config_window.geometry(f"250x{90+num_config_options*40}")

    def light_driver_dropdown_callback(*args):
        # Hide all the config frames
        for frame in config_frames.values():
            frame.grid_forget()
        # Show the config frame for the selected light driver
        driver = light_driver_var.get()
        config_frames[driver].grid(row=2, column=0, columnspan=2)
        # Load Config to Entry Fields
        load_config_to_entry_fields(driver)
        resize_window()
        root.update()

    position_label = ttk.Label(
        light_config_window, text=f"Configuring Light at {row}, {column}")
    position_label.grid(row=0, column=0, columnspan=2)

    # Because there are many different types of light drivers, we will use a dropdown menu to select the light driver
    light_driver_label = ttk.Label(light_config_window, text="Light Driver")
    light_driver_label.grid(row=1, column=0)
    light_driver_var = tk.StringVar()
    light_driver_var.set("espmega")
    # Switch to the correct light driver config frame based on the selected light driver
    drivers = list(config_options.keys())
    light_driver_dropdown = tk.OptionMenu(
        light_config_window, light_driver_var, *drivers,command=light_driver_dropdown_callback)
    light_driver_dropdown.grid(row=1, column=1)


    for device, config_option in config_options.items():
        config_vars[device] = {}
        # Create a frame to hold the config options for each light driver
        config_frames[device] = tk.Frame(light_config_window)
        for config_option in config_options[device]:
            config_label_text = config_option.replace("_", " ").title()
            config_option_label = ttk.Label(
                config_frames[device], text=config_label_text)
            config_option_label.pack(padx=20, anchor="center")
            config_option_var = tk.StringVar()
            config_option_entry = ttk.Entry(config_frames[device], textvariable=config_option_var, width=35)
            config_option_entry.pack(padx=20, anchor="center")
            config_vars[device][config_option] = config_option_var

    # Each light driver has different configuration options, different configuration options will be shown depending on the selected light driver
    driver = get_driver_from_json()
    # Load the coreesponding frame for the selected light driver
    config_frames[driver].grid(row=2, column=0, columnspan=2)
    # Load Config to Entry Fields
    load_config_to_entry_fields(driver)
    # Set the light driver dropdown to the correct value
    light_driver_var.set(driver)
    root.update()
    # Create a button to save the light config and close the window
    submit_button = ttk.Button(
        light_config_window, text="Save", command=submit_light_config)
    submit_button.grid(row=3, column=0, columnspan=2,pady=5,padx=85)
    resize_window()
    light_config_window.mainloop()


def render_frame_at_index(frame_index: int):
    frame = frames[frame_index]
    render_frame(frame)

def frame_forward():
    frame_index = slider.get()
    if frame_index < len(frames)-1:
        slider.set(frame_index+1)
        render_frame_at_index(frame_index+1)
    if frame_index == len(frames)-1 and repeat_var.get():
        slider.set(0)
        render_frame_at_index(0)
    root.update()

def frame_backward():
    frame_index = slider.get()
    if frame_index > 0:
        slider.set(frame_index-1)
        render_frame_at_index(frame_index-1)
    if frame_index == 0 and repeat_var.get():
        slider.set(len(frames)-1)
        render_frame_at_index(len(frames)-1)
    root.update()

def reconnect_light_controllers():
    global light_grid
    global design_mode
    old_light_map = light_grid.light_map
    light_grid = LightGrid(design_mode=design_mode)
    light_grid.read_light_map(old_light_map)
    render_frame_at_index(slider.get())
    root.update()


frames = [[[0]*light_grid.columns]*light_grid.rows]

root = tk.Tk()

root.title(WINDOW_TITLE)
icon = ImageTk.PhotoImage(icon_image)
root.wm_iconphoto(True, icon)


# Create a label for the title
title_label = ttk.Label(root, text=WINDOW_TITLE, font=("Helvetica", 36, "bold"), foreground="gray26")
title_label.pack()

# Create another frame to the bottom
buttom_frame = ttk.Frame(root)
buttom_frame.pack(side="bottom", padx=10)  # Add padding to the right frame

# Create a grid to hold the playback controls
playback_grid = ttk.Frame(buttom_frame)
playback_grid.pack()

playback_status_frame = ttk.Frame(playback_grid)

# Create a text label for the playback controls
playback_label = ttk.Label(
    playback_status_frame, text="Playback Controls", font=("Arial", 10))
playback_label.pack()

# Create a text label to show the current playback status
playback_status_label = ttk.Label(playback_status_frame, text=PLAYBACK_STATUS_STOPPED)
playback_status_label.pack()

playback_status_frame.pack(side="left")

# Create a separator to seperate the playback controls from the playback status
separator = ttk.Separator(playback_grid, orient="vertical")
separator.pack(side="left", padx=10, fill="y")

# Create a frame to hold the button section of the playback controls
playback_section = ttk.Frame(playback_grid)
playback_section.pack(side="left")

# Create a frame to hold the playback controls
playback_button_frame = ttk.Frame(playback_section)
playback_button_frame.pack()

# Create a button to play the recorded frames
play_button = ttk.Button(playback_button_frame, text="Play", command=play_frames)
play_button.pack(side="left")

# Create a button to pause the animation
pause_button = ttk.Button(playback_button_frame, text="Pause", command=pause_frames)
pause_button.pack(side="left")

# Create a button to stop the animation
stop_button = ttk.Button(playback_button_frame, text="Stop", command=stop_frames)
stop_button.pack(side="left")

# Create a frame to hold the repeat toggle and the scrubing controls
manipulation_frame = ttk.Frame(playback_section)
manipulation_frame.pack()

# Create a button that goes to the previous frame
button_previous_frame = ttk.Button(
    manipulation_frame, text="Previous Frame", command=frame_backward)
button_previous_frame.pack(side="left")

# Create a repeat toggle
repeat_var = tk.BooleanVar()
repeat_toggle = ttk.Checkbutton(
    manipulation_frame, text="Repeat", variable=repeat_var)
repeat_toggle.pack(side="left")

# Create a button that goes to the next frame
button_next_frame = ttk.Button(
    manipulation_frame, text="Next Frame", command=frame_forward)
button_next_frame.pack(side="right")

# Add a separator to seperate the playback controls from bpm controls
separator = ttk.Separator(playback_grid, orient="vertical")
separator.pack(side="left", padx=10, fill="y")

# Create a scale to adjust playback speed
speed_scale = tk.Scale(playback_grid, from_=MIN_BPM, to=MAX_BPM,
                       orient="horizontal", label="BPM", resolution=0.1)
speed_scale.set(120)
speed_scale.pack()

# Create a separator to seperate the slider from the top frame
separator = ttk.Separator(buttom_frame, orient="horizontal")
separator.pack(fill="x", pady=10)

# Create a slider to scrub through recorded frames
slider = tk.Scale(buttom_frame, label="Timeline", from_=0, to=len(
    frames)-1, orient="horizontal", command=scrub_frames,length=root.winfo_width()*0.9)
slider.pack()

help_label = ttk.Label(
    buttom_frame, text="Left click to toggle a light.\nRight click to configure a light.", font=("Arial", 12), justify="center")
help_label.pack()

if (design_mode):
    # Create a text label for the design mode
    design_mode_label = ttk.Label(
        buttom_frame, text="You are currently in design mode.\nIn this mode, physical lights will not be controlled.", font=("Arial", 12, "bold"), foreground="red", justify="center")
    design_mode_label.pack()

# Create a text label for the author
author_label = ttk.Label(
    buttom_frame, text="SIWAT SYSTEM 2023", font=("Arial", 12))
author_label.pack()

# Create another frame to the right
management_frame = ttk.Frame(root)
management_frame.pack(side="right", padx=10)  # Add padding to the right frame

playback_frame = ttk.Frame(management_frame)
playback_frame.pack()

# Create a text label for the record controls
record_label = ttk.Label(playback_frame, text="Record Controls", font=("Arial", 10))
record_label.pack()

# Create a separator to seperate the record controls from the label
separator = ttk.Separator(playback_frame, orient="horizontal")
separator.pack(fill="x")

# Create a button to add a frame to the end of the animation
add_frame_button = tk.Button(
    playback_frame, text="Add Frame", command=add_frame, height=4, width=15, bg="green", fg="white")
add_frame_button.pack(pady=5)

# Create a button to record a frame to the current frame
record_frame_button = tk.Button(
    playback_frame, text="Record Frame", command=record_frame, height=4, width=15, bg="red", fg="white")
record_frame_button.pack(pady=5)

# Create a button to delete the current frame
delete_frame_button = tk.Button(
    playback_frame, text="Delete Frame", command=delete_frame, height=4, width=15, bg="firebrick4", fg="white")
delete_frame_button.pack(pady=5)

# Create a separator to seperate the record controls from the label
separator = ttk.Separator(playback_frame, orient="horizontal")
separator.pack(fill="x")

# Create a text label for the frame manipulation controls
frame_manipulation_label = ttk.Label(playback_frame, text="Move Current Frame", font=("Arial", 10))
frame_manipulation_label.pack()

# Create a frame to hold the frame manipulation buttons (move frame left and move frame right)
frame_manipulation_frame = ttk.Frame(playback_frame)
frame_manipulation_frame.pack()

# Create a button to move the current frame left
move_frame_left_button = tk.Button(
    frame_manipulation_frame, text="Left", command=move_frame_left, height=2, width=8, bg="orange", fg="black")
move_frame_left_button.grid(row=1, column=0, pady=5)

# Create a button to move the current frame right
move_frame_right_button = tk.Button(
    frame_manipulation_frame, text="Right", command=move_frame_right, height=2, width=8, bg="orange", fg="black")
move_frame_right_button.grid(row=1, column=1, pady=5)

# Create a separator to seperate the frame manipulation controls from the utility
separator = ttk.Separator(playback_frame, orient="horizontal")
separator.pack(fill="x")

# Create a text label for the utility
utility_label = ttk.Label(management_frame, text="BPM Counter", font=("Arial", 10))
utility_label.pack()



bpm_samples = []

def bpm_counter_callback():
    global last_press_time, bpm_samples
    current_time = time.time()
    if last_press_time is not None:
        bpm = 60 / (current_time - last_press_time)
        bpm_samples.append(bpm)
        if len(bpm_samples) > 5:
            bpm_samples = bpm_samples[-5:]  # Keep only the last 5 samples
        bpm_average = statistics.mean(bpm_samples)
        if len(bpm_samples) == 1:
            bpm_filtered = bpm_samples
        else:
            bpm_filtered = [b for b in bpm_samples if abs(b - bpm_average) <= 2 * statistics.stdev(bpm_samples)]
        bpm = statistics.mean(bpm_filtered)
        bpm_counter_button.config(text=f"{bpm:.2f} BPM")
        
        # Change button color based on BPM
        if bpm < 100:
            bpm_counter_button.config(bg="blue")
        elif bpm >= 100 and bpm < 150:
            bpm_counter_button.config(bg="green")
        else:
            bpm_counter_button.config(bg="red")
        
    last_press_time = current_time

last_press_time = None

# Create a BPM counter button
bpm_counter_button = tk.Button(
    management_frame, text="Click Me!", command=bpm_counter_callback, height=2, width=15, bg="blue", fg="white")
bpm_counter_button.pack(pady=5)

# Create a button to apply the BPM to the speed scale
bpm_apply_button = tk.Button(
    management_frame, text="Apply BPM", command=lambda: speed_scale.set(bpm_counter_button.cget("text").split(" ")[0]), height=2, width=15, bg="blue", fg="white")
bpm_apply_button.pack(pady=5)

lightgrid_frame = ttk.Frame(root)
lightgrid_frame.pack()


def resize_elements(event):
    width = (root.winfo_width() - management_frame.winfo_width()) // columns*0.9
    height = (root.winfo_height() - buttom_frame.winfo_height() -
              title_label.winfo_height())/rows*0.95
    for i in range(rows):
        for j in range(columns):
            element = lightgrid_frame.grid_slaves(row=i, column=j)[0]
            element.config(width=width, height=height)
    slider.config(length=root.winfo_width()*0.9)
    speed_scale.config(length=(root.winfo_width()-playback_section.winfo_width()-playback_status_frame.winfo_width()-20)*0.8)

for i in range(rows):
    for j in range(columns):
        element = tk.Frame(lightgrid_frame, width=50, height=50,
                           bg="white", highlightthickness=1, highlightbackground="black")
        element.grid(row=i, column=j)
        # Bind left mouse click event to change_color function
        element.bind("<Button-1>", change_color)
        # Bind right mouse click event to change_light_config function
        element.bind("<Button-3>", change_light_config)


def load_animation():
    global frames
    filename = filedialog.askopenfilename(filetypes=[FILE_TYPE_JSON])
    if filename:
        try:
            with open(filename, "r") as file:
                temp_frames = json.load(file)
                # Check if the animation is empty
                if len(temp_frames) == 0:
                    raise ValueError("Animation cannot be empty.")
                # Check if the animation has the same dimensions as the light map
                if len(temp_frames[0]) != len(light_grid.light_map) or len(temp_frames[0][0]) != len(light_grid.light_map[0]):
                    raise ValueError(
                        "The animation must have the same dimensions as the light map.")
                # Check the animation for invalid frames
                for frame in temp_frames:
                    for row in frame:
                        for light in row:
                            # Check if the light is a boolean value or an integer value of 0 or 1
                            if not isinstance(light, bool) and not isinstance(light, int) or (isinstance(light, int) and (light != 0 and light != 1)):
                                raise ValueError(
                                    "The animation must only contain boolean values.")
                frames = temp_frames
            slider.config(to=len(frames)-1)  # Update the slider range
            slider.set(0)  # Set the slider value to the first frame
        except FileNotFoundError:
            messagebox.showerror(
                MSG_FILE_NOT_FOUND_TITLE, f"The file {filename} could not be found.")
        except Exception as e:
            messagebox.showerror(MSG_LOAD_ERROR_TITLE, f"{e}\nAre you sure this is a valid animation file?")

def new_animation():
    global frames
    frames = [[[0]*light_grid.columns]*light_grid.rows]
    slider.config(to=len(frames)-1)  # Update the slider range
    slider.set(0)  # Set the slider value to the first frame
    render_frame_at_index(0)


def run_script(filename: str):
    def import_from_file(module_name, file_path):
        spec = importlib_util.spec_from_file_location(module_name, file_path)
        module = importlib_util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    global playback_active
    global script_active

    if filename:
        try:
            print(f'Loaded : {filename.split(".")[0]}')
            CustomUserScript = import_from_file(filename.split(".")[0], filename).CustomUserScript
        except FileNotFoundError:
            messagebox.showerror(
                "File Not Found", f"The file {filename} could not be found.")
        except Exception as e:
            messagebox.showerror(MSG_LOAD_ERROR_TITLE, f"{e}\nAre you sure this is a valid Python script?")
    # At this point, the class "CustomUserScript" should be defined
    # Check if the class is defined
    if "CustomUserScript" not in locals():
        messagebox.showerror(MSG_SCRIPT_ERROR_TITLE, "The script must define a class called CustomUserScript.")
        return

    # Check if the class is a subclass of UserScript
    if not issubclass(CustomUserScript, UserScript):
        messagebox.showerror(MSG_SCRIPT_ERROR_TITLE, "The class CustomUserScript must be a subclass of UserScript.")
        return

    def logger_func(message: any):
        print(message)
        message = str(message)
        # Add a timestamp and frame number to the message, note that the timestamp is the time since the script started
        message = f"[{script.frame_count}, {perf_counter() - begin_time:.2f}s] {message}"
        # Add the message to the textbox
        script_output_textbox.config(state="normal")
        script_output_textbox.insert(tk.END, message + "\n")
        script_output_textbox.see(tk.END)
        script_output_textbox.config(state="disabled")
        root.update()

    # Instantiate the class
    script = CustomUserScript(rows, columns, set_tile_state, get_tile_state, logger_func)

    # Stop Playback if it is active
    if playback_active:
        playback_active = False
    
    # All controls except the speed scale and the BPM counter button
    add_frame_button.config(state="disabled")
    record_frame_button.config(state="disabled")
    delete_frame_button.config(state="disabled")
    move_frame_left_button.config(state="disabled")
    move_frame_right_button.config(state="disabled")
    button_previous_frame.config(state="disabled")
    button_next_frame.config(state="disabled")
    slider.config(state="disabled")
    play_button.config(state="disabled")
    pause_button.config(state="disabled")
    stop_button.config(state="disabled")
    repeat_toggle.config(state="disabled")
    # Lock Run Script button
    file_menu.entryconfig(4, state="disabled")
    # Lock All Quick Load Menu
    for i in range(5):
        quick_run_menu.entryconfig(i, state="disabled")
        quick_run_menu.entryconfig(i+7, state="disabled")
    playback_status_label.config(text=PLAYBACK_STATUS_SCRIPTED)

    script_active = True

    # Create a new window to display the script controls
    script_controls_window = tk.Toplevel(root)
    script_controls_window.title("Script Runner")
    icon = ImageTk.PhotoImage(icon_image)
    script_controls_window.wm_iconphoto(True, icon)
    script_controls_window.geometry("500x130")

    # Set minimum size
    script_controls_window.minsize(500, 500)
    
    # Create the top information frame
    top_frame = ttk.Frame(script_controls_window)
    top_frame.pack(pady=5)

    # Add a label to display the script name
    script_name_label = ttk.Label(top_frame, text=f"Script: {filename.split('/')[-1]}")
    script_name_label.pack()

    # Add a label to display the script status
    script_status_label = ttk.Label(top_frame, text=PLAYBACK_STATUS_SCRIPTED)
    script_status_label.pack()

    # Add a label to display the current frame number
    script_frame_label = ttk.Label(top_frame, text="Frame: 0")
    script_frame_label.pack()

    # Add a label to display the current time
    script_time_label = ttk.Label(top_frame, text="Time Elapsed: 0")
    script_time_label.pack()

    # Add a frame to hold the script output textbox
    script_output_frame = ttk.Frame(script_controls_window)
    script_output_frame.pack()

    # Add a textbox to display the script output
    script_output_textbox = tk.Text(script_output_frame)

    # # Disable editing
    script_output_textbox.config(state="disabled")
    # Span the textbox across the entire frame
    script_output_textbox.pack(fill="both", expand=True)

    def stop_script():
        script.active = False

    def restart_script():
        script.active = False
        start_time = perf_counter()
        while script.executing:
            if perf_counter() - start_time >= 15000:
                messagebox.showerror(MSG_SCRIPT_ERROR_TITLE, "The script is taking too long to stop.\nProgram will now restart to prevent the program from freezing.")
                restart()
            root.update()
            root.update_idletasks()
        script_controls_window.destroy()
        run_script(filename)

    # Create a buttom frame to hold the controls
    buttom_frame = ttk.Frame(script_controls_window)

    # Add a button to restart the script
    script_restart_button = ttk.Button(buttom_frame, text="Restart", command=restart_script)
    script_restart_button.pack(pady=5)

    # Add a stop button to stop the script
    script_stop_button = ttk.Button(buttom_frame, text="Stop", command=stop_script)
    script_stop_button.pack(pady=5)

    # Pack the buttom frame
    buttom_frame.pack()

    def on_resize(event):
        # Resize the textbox to fit the window, note that since only the height is changed, the width does not need to be changed
        script_output_frame.config(height=script_controls_window.winfo_height() - top_frame.winfo_height() - buttom_frame.winfo_height()-20, width=script_controls_window.winfo_width()-20)
        root.update()
    script_controls_window.bind("<Configure>", on_resize)

    start_time = perf_counter()
    begin_time = perf_counter()
    ignore_execution_flag = False
    while True:
        if not script.active:
            break
        # Check if script window is closed
        if not script_controls_window.winfo_exists():
            script.active = False
            break
        # Calculate delay in seconds from bpm
        delay = 60 / speed_scale.get()
        if perf_counter() - start_time >= delay:
            start_time = perf_counter()
            time_epoch = perf_counter() - begin_time
            # Execute the script using try-except to catch errors
            # This script will be written by the user and might contain errors
            try:
                script.__draw_frame__(time_epoch)
            except Exception as e:
                messagebox.showerror(MSG_SCRIPT_ERROR_TITLE, traceback.format_exc())
                # Stop the script
                script.active = False
                # Set the ignore execution flag to true to prevent the program from waiting for the script to stop
                ignore_execution_flag = True
                break
            # Update the frame label
            script_frame_label.config(text=f"Frame: {script.frame_count}")
        # Update the time label
        script_time_label.config(text=f"Time Elapsed: {perf_counter() - begin_time:.2f} seconds")
        root.update()
        root.update_idletasks()
    stop_wait_time = 15000
    stop_time = perf_counter()
    # script.execuiting is meant to be set by the script itself to indicate that it is still running
    while script.executing and not ignore_execution_flag:
        if perf_counter() - stop_time >= stop_wait_time:
            messagebox.showerror(MSG_SCRIPT_ERROR_TITLE, "The script is taking too long to stop.\nProgram will now restart to prevent the program from freezing.")
            restart()
        root.update()
        root.update_idletasks()
    playback_active = False
    script_controls_window.destroy()
    # Re-enable all controls
    add_frame_button.config(state="normal")
    record_frame_button.config(state="normal")
    delete_frame_button.config(state="normal")
    move_frame_left_button.config(state="normal")
    move_frame_right_button.config(state="normal")
    button_previous_frame.config(state="normal")
    button_next_frame.config(state="normal")
    slider.config(state="normal")
    play_button.config(state="normal")
    pause_button.config(state="normal")
    stop_button.config(state="normal")
    repeat_toggle.config(state="normal")
    # Unlock Run Script button
    file_menu.entryconfig(4, state="normal")
    # Unlock All Quick Load Menu
    quick_run_menu.entryconfig(0, state="normal")
    for i in range(5):
        quick_run_menu.entryconfig(i, state="normal")
        quick_run_menu.entryconfig(i+7, state="normal")
    playback_status_label.config(text=PLAYBACK_STATUS_STOPPED)
    script_active = False
render_frame_at_index(0)

def generate_template_script():
    # Ask the user where to save the script
    filename = filedialog.asksaveasfilename(
        defaultextension=".py", filetypes=[FILE_TYPE_PYTHON])
    # Copy the template script from the module directory to the specified location
    if filename:
        try:
            shutil.copyfile(os.path.join(os.path.dirname(__file__), "template_script.py"), filename)
        except Exception as e:
            messagebox.showerror("Save Error", f"{e}")

root.bind("<Configure>", resize_elements)


def run_script_prompt():
    filename = filedialog.askopenfilename(filetypes=[FILE_TYPE_PYTHON])
    run_script(filename)

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create the file menu
file_menu = tk.Menu(menu_bar, tearoff=False)
file_menu.add_command(label="New Animation", command=new_animation)
file_menu.add_command(label="Save Animation", command=save_animation)
file_menu.add_command(label="Load Animation", command=load_animation)
file_menu.add_separator()
file_menu.add_command(label="Run Script", command=run_script_prompt)
file_menu.add_command(label="Generate Template Script", command=generate_template_script)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create the controller menu
controller_menu = tk.Menu(menu_bar, tearoff=False)
controller_menu.add_command(
    label="Reconnect Controllers", command=reconnect_light_controllers)
controller_menu.add_command(
    label="Reconfigure Controllers", command=restart)
controller_menu.add_separator()
controller_menu.add_command(
    label="Generate Light Map", command=open_generate_light_map_template_window)
menu_bar.add_cascade(label="Controllers", menu=controller_menu)

def load_animation_at_slot(slot: int):
    global frames
    filename = animation_quick_load_slots[slot-1]
    if (filename == None):
        save_animation_at_slot(slot)
        return
    if filename:
        try:
            with open(filename, "r") as file:
                temp_frames = json.load(file)
                # Check if the animation is empty
                if len(temp_frames) == 0:
                    raise ValueError("Animation cannot be empty.")
                # Check if the animation has the same dimensions as the light map
                if len(temp_frames[0]) != len(light_grid.light_map) or len(temp_frames[0][0]) != len(light_grid.light_map[0]):
                    raise ValueError(
                        "The animation must have the same dimensions as the light map.")
                # Check the animation for invalid frames
                for frame in temp_frames:
                    for row in frame:
                        for light in row:
                            # Check if the light is a boolean value or an integer value of 0 or 1
                            if not isinstance(light, (bool, int)) or (isinstance(light, int) and light not in (0, 1)):
                                raise ValueError(
                                    "The animation must only contain boolean values.")
                frames = temp_frames
            slider.config(to=len(frames)-1)  # Update the slider range
            slider.set(0)  # Set the slider value to the first frame
            # Update quick load menu
            quick_run_menu.entryconfig(slot-1, label=f"Animation Slot {slot}: {filename.split('/')[-1]}")
        except FileNotFoundError:
            messagebox.showerror(
                "File Not Found", f"The file {filename} could not be found.")
        except Exception as e:
            messagebox.showerror(MSG_LOAD_ERROR_TITLE, f"{e}\nAre you sure this is a valid animation file?")
        render_frame_at_index(0)
        if (instant_playback_var.get()):
            play_frames()

# Put script filenames in the quick load menu
def save_script_at_slot(slot: int):
    global script_quick_load_slots
    # Ask the user where the script is located
    filename = filedialog.askopenfilename(filetypes=[FILE_TYPE_PYTHON])
    if filename:
        script_quick_load_slots[slot-1] = filename
        quick_run_menu.entryconfig(slot+6, label=f"Script Slot {slot}: {filename.split('/')[-1]}")

# Put animation filenames in the quick load menu
def save_animation_at_slot(slot: int):
    global animation_quick_load_slots
    # Ask the user where the animation is located
    filename = filedialog.askopenfilename(filetypes=[FILE_TYPE_JSON])
    if filename:
        animation_quick_load_slots[slot-1] = filename
        quick_run_menu.entryconfig(slot-1, label=f"Animation Slot {slot}: {filename.split('/')[-1]}")

# Run the script at the specified slot if it is not empty
def load_script_at_slot(slot: int):
    filename = script_quick_load_slots[slot-1]
    print(filename)
    if (filename == None):
        save_script_at_slot(slot)
        return
    run_script(filename)

def clear_animation_slot(slot: int):
    global animation_quick_load_slots
    animation_quick_load_slots[slot-1] = None
    quick_run_menu.entryconfig(slot-1, label=f"Animation Slot {slot}: Empty")

def clear_script_slot(slot: int):
    global script_quick_load_slots
    script_quick_load_slots[slot-1] = None
    quick_run_menu.entryconfig(slot+6, label=f"Script Slot {slot}: Empty")

instant_playback_var = tk.BooleanVar()

# Create the Quick Run menu
quick_run_menu = tk.Menu(menu_bar, tearoff=False)
quick_run_menu.add_command(label="Animation Slot 1: Empty", command=lambda: load_animation_at_slot(1))
quick_run_menu.add_command(label="Animation Slot 2: Empty", command=lambda: load_animation_at_slot(2))
quick_run_menu.add_command(label="Animation Slot 3: Empty", command=lambda: load_animation_at_slot(3))
quick_run_menu.add_command(label="Animation Slot 4: Empty", command=lambda: load_animation_at_slot(4))
quick_run_menu.add_command(label="Animation Slot 5: Empty", command=lambda: load_animation_at_slot(5))
quick_run_menu.add_checkbutton(label="Instant Playback (Disabled)", variable=instant_playback_var, command=lambda: quick_run_menu.entryconfig(5,label="Instant Playback (Enabled)" if instant_playback_var.get() else "Instant Playback (Disabled)"))
quick_run_menu.add_separator()
quick_run_menu.add_command(label="Script Slot 1: Empty", command=lambda: load_script_at_slot(1))
quick_run_menu.add_command(label="Script Slot 2: Empty", command=lambda: load_script_at_slot(2))
quick_run_menu.add_command(label="Script Slot 3: Empty", command=lambda: load_script_at_slot(3))
quick_run_menu.add_command(label="Script Slot 4: Empty", command=lambda: load_script_at_slot(4))
quick_run_menu.add_command(label="Script Slot 5: Empty", command=lambda: load_script_at_slot(5))
quick_run_menu.add_separator()
# Create a submenu to house the clear menu
clear_menu = tk.Menu(quick_run_menu, tearoff=False)
clear_menu.add_command(label="Animation Slot 1", command=lambda: clear_animation_slot(1))
clear_menu.add_command(label="Animation Slot 2", command=lambda: clear_animation_slot(2))
clear_menu.add_command(label="Animation Slot 3", command=lambda: clear_animation_slot(3))
clear_menu.add_command(label="Animation Slot 4", command=lambda: clear_animation_slot(4))
clear_menu.add_command(label="Animation Slot 5", command=lambda: clear_animation_slot(5))
clear_menu.add_separator()
clear_menu.add_command(label="Script Slot 1", command=lambda: clear_script_slot(1))
clear_menu.add_command(label="Script Slot 2", command=lambda: clear_script_slot(2))
clear_menu.add_command(label="Script Slot 3", command=lambda: clear_script_slot(3))
clear_menu.add_command(label="Script Slot 4", command=lambda: clear_script_slot(4))
clear_menu.add_command(label="Script Slot 5", command=lambda: clear_script_slot(5))
clear_menu.add_separator()
clear_menu.add_command(label="Clear All Animation Slots", command=lambda: [clear_animation_slot(i) for i in range(1, 6)])
clear_menu.add_command(label="Clear All Script Slots", command=lambda: [clear_script_slot(i) for i in range(1, 6)])
clear_menu.add_command(label="Clear All", command=lambda: [clear_animation_slot(i) for i in range(1, 6)] + [clear_script_slot(i) for i in range(1, 6)])
quick_run_menu.add_cascade(label="Clear Slot", menu=clear_menu)
menu_bar.add_cascade(label="Quick Load", menu=quick_run_menu)

# Populate the quick run menu with the filenames in the quick load slots
for i in range(5):
    if animation_quick_load_slots[i] != None:
        quick_run_menu.entryconfig(i, label=f"Animation Slot {i+1}: {animation_quick_load_slots[i].split('/')[-1]}")
    if script_quick_load_slots[i] != None:
        quick_run_menu.entryconfig(i+7, label=f"Script Slot {i+1}: {script_quick_load_slots[i].split('/')[-1]}")

def open_about_popup():
    about_popup = tk.Toplevel(root)
    about_popup.title("About")
    icon = ImageTk.PhotoImage(icon_image)
    about_popup.iconbitmap.wm_iconphoto(True, icon)
    about_popup.geometry("350x110")
    about_popup.resizable(False, False)

    # Create a label for the title
    title_label = ttk.Label(about_popup, text=WINDOW_TITLE, font=("Arial", 24))
    title_label.pack()

    # Create a label for the author
    author_label = ttk.Label(about_popup, text="Made by Siwat Sirichai")
    author_label.pack()

    # Create link to the github repository
    def open_github():
        webbrowser.open("https://github.com/SiwatINC/espmega-lightshow/")
    github_link = ttk.Label(about_popup, text="GitHub Repository", foreground="blue", cursor="hand2")
    github_link.pack()
    github_link.bind("<Button-1>", lambda e: open_github())

    # Create a label for the company name
    company_label = ttk.Label(about_popup, text="SIWAT SYSTEM 2023")
    company_label.pack()

# Check for updates using pip
def check_for_updates():
    # Run pip in a subprocess
    process = subprocess.Popen(["pip", "install", "--upgrade", "espmega-lightshow"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    # Check if pip returned an error
    if process.returncode != 0:
        messagebox.showerror("Update Error", f"An error occured while checking for updates.\n{stderr.decode('utf-8')}")
    else:
        return_message = stdout.decode("utf-8")
        # Get current version by running pip show
        process = subprocess.Popen(["pip", "show", "espmega-lightshow"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        # Check if pip returned an error
        if process.returncode != 0:
            messagebox.showerror("Update Error", f"An error occured while checking for updates.\n{stderr.decode('utf-8')}")
            return
        # Extract the version number from the output
        current_version = re.search(r"Version: (.*)", stdout.decode("utf-8")).group(1)
        # Check if pip returned a message
        if ("Collecting espmega-lightshow" in return_message):
            messagebox.showinfo("Update", f"Updated to version {current_version}\nPlease restart the program to apply the update.")
        else:
            messagebox.showinfo("Update", f"No updates found\nYou are already on the latest version ({current_version}).")

# Create the help menu
help_menu = tk.Menu(menu_bar, tearoff=False)
help_menu.add_command(label="About", command=open_about_popup)
help_menu.add_command(label="Documentation", command=lambda: webbrowser.open("https://github.com/SiwatINC/espmega-lightshow/wiki"))
help_menu.add_command(label="Check for Updates", command=check_for_updates)
menu_bar.add_cascade(label="Help", menu=help_menu)


# Set the size of the root window
root.geometry("1000x800")

def handle_spacebar(event):
    # Inclement the current frame by 1 then render the frame
    # unless the current frame is the last frame then loop back to the first frame and render it
    if slider.get() == len(frames)-1:
        slider.set(0)
        render_frame_at_index(0)
    else:
        slider.set(slider.get()+1)
        render_frame_at_index(slider.get())

def handle_up_arrow(event):
    # Increase the bpm by 0.5 if increasing the bpm will not cause the value to exceed 200 if it exceeds 200, set it to 200
    if speed_scale.get() + 0.5 <= 200:
        speed_scale.set(speed_scale.get()+0.5)
    else:
        speed_scale.set(200)

def handle_down_arrow(event):
    # Decrease the bpm by 0.5 if decreasing the bpm will not cause the value to go below 40 if it goes below 40, set it to 40
    if speed_scale.get() - 0.5 >= 40:
        speed_scale.set(speed_scale.get()-0.5)
    else:
        speed_scale.set(40)

def handle_left_arrow(event):
    # Decrement the current frame by 1 then render the frame
    # unless the current frame is the first frame then loop back to the last frame and render it
    if slider.get() == 0:
        slider.set(len(frames)-1)
        render_frame_at_index(len(frames)-1)
    else:
        slider.set(slider.get()-1)
        render_frame_at_index(slider.get())

def handle_right_arrow(event):
    # Increment the current frame by 1 then render the frame
    # unless the current frame is the last frame then loop back to the first frame and render it
    if slider.get() == len(frames)-1:
        slider.set(0)
        render_frame_at_index(0)
    else:
        slider.set(slider.get()+1)
        render_frame_at_index(slider.get())

root.bind("<space>", handle_spacebar)
root.bind("<Up>", handle_up_arrow)
root.bind("<Down>", handle_down_arrow)
root.bind("<Left>", handle_left_arrow)
root.bind("<Right>", handle_right_arrow)


root.mainloop()

# Write Quick Load data to file
with open(CONFIG_FILE, "w") as file:
    json.dump({"light_server": light_server, "light_server_port": light_server_port,
                "rapid_mode": rapid_mode, "light_map_file": light_map_file, "design_mode": design_mode,
                "script_quick_load_slots": script_quick_load_slots, "animation_quick_load_slots": animation_quick_load_slots}, file)

# Take all connected controllers out of rapid response mode
if rapid_mode:
    for driver in light_grid.drivers.values():
        driver.disable_rapid_response_mode()
