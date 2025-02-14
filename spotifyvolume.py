import os
import sys
import logging
import tkinter as tk
import ctypes
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import keyboard
import configparser

# Set up logging to capture errors and crashes
log_file = 'crashlog.txt'
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function to log uncaught exceptions
def log_exception(exc_type, exc_value, exc_tb):
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_tb))

# Install the custom exception hook to log uncaught exceptions
sys.excepthook = log_exception

# config for properties
config_file = 'config.properties'

# Check if the config file exists, create it if it doesn't
if not os.path.exists(config_file):
    config = configparser.ConfigParser()
    
    # Add default values
    config['Settings'] = {
        'client_id': 'your-client-id',
        'client_secret': 'your-client-secret',
        'VolumeDown': 'F23',
        'VolumeUp': 'F24',
        'VolumePercentage': '5',
        'VolumeDefault': '50'
    }
    
    # Write the config file
    with open(config_file, 'w') as configfile:
        config.write(configfile)

# Read the config file
config = configparser.ConfigParser()
config.read(config_file)

client_id = config.get('Settings', 'client_id')
client_secret = config.get('Settings', 'client_secret')

VolumeUp = config.get('Settings', 'VolumeUp')
VolumeDown = config.get('Settings', 'VolumeDown')
VolumePercentage = int(config.get('Settings', 'VolumePercentage'))
VolumeDefault = int(config.get('Settings', 'VolumeDefault'))

# Set the app user model ID for the taskbar icon
myappid = "spopipy"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Create the Tkinter window
root = tk.Tk()
root.iconbitmap("ICON/spopipy.ico")
root.title("Spotify Volume Control")

# Add a label or something to interact with
label = tk.Label(root, text=f"Control your Spotify volume using {VolumeDown} and {VolumeUp}", font=("Arial", 12))
label.pack(padx=10, pady=10)

# Spotify OAuth credentials
redirect_uri = "http://localhost:8000"
scope = "user-read-playback-state,user-modify-playback-state"

# Function to change volume
def volumeChange(volume):
    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=scope,
                open_browser=False
            )
        )
        sp.volume(volume)
    except Exception as e:
        logging.error(f"Error changing volume: {e}")

volume = VolumeDefault

def decrease_volume():
    global volume
    volume = max(0, volume - VolumePercentage)
    volumeChange(volume)
    label.config(text=f"\tVolume: {volume}%\t")

def increase_volume():
    global volume
    volume = min(100, volume + VolumePercentage)
    volumeChange(volume)
    label.config(text=f"\tVolume: {volume}%\t")

keyboard.add_hotkey(VolumeDown, decrease_volume)
keyboard.add_hotkey(VolumeUp, increase_volume)

# Run the Tkinter main loop
try:
    root.mainloop()
except Exception as e:
    logging.error(f"Error running Tkinter main loop: {e}")
