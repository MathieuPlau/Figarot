import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

with open(CONFIG_FILE, "r") as file:
    settings = json.load(file)

SAMPLES_PATH = settings["samples_path"]
NETWORK = settings["network"]
DEBUG = settings["debug"]
PYGAME_MIXER = settings["pygame_mixer"]
AUDIO_SETTINGS = settings["audio_settings"]
CHAOS_MODE = settings["chaos_mode"]