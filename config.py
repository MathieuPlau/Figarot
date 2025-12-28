import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

with open(CONFIG_FILE, "r") as file:
    settings = json.load(file)

class Config:
    SAMPLES_PATH = settings.get("samples_path", "./samples/")
    NETWORK = settings.get("network")
    DEBUG = settings.get("debug", True)
    PYGAME_MIXER = settings.get("pygame_mixer")
    AUDIO_SETTINGS = settings.get("audio_settings")
    CHAOS_MODE = settings.get("chaos_mode")