import os
import simpleaudio as sa
import threading
import pygame
from config import Config
from pathlib import Path

# Initialize pygame mixer
pygame.mixer.init(Config.pygame_mixer['frequency'],
                   Config.pygame_mixer['size'],
                   Config.pygame_mixer['channels'],
                   Config.pygame_mixer['buffer'])

# Thread-safe list to store active sounds
active_sounds_lock = threading.Lock()
active_sounds = []

# Returns directories from the given path
def parse_directories(path):
    directories = []
    with os.scandir(path) as it:
        for entry in it:
            # Avoid git directory to be parsed
            if (entry.is_dir() and entry.name != ".git"):
                directories.append({
                    'name': entry.name,
                    'type': 'folder'
                })
    return directories 

# Returns files from the given directory
def parse_files(directory_path): 
    if(Config.DEBUG):
        print("DEBUG: " + directory_path)   
    
    files = []
    with os.scandir(directory_path) as it:
        for entry in it:
            if entry.is_file():
                files.append({
                    'name': entry.name,
                    'type': 'file'
                })
    return files

def play_audio_file(sound_path):
    if(Config.DEBUG):
        print("DEBUG: " + sound_path)

    file_path = Path(sound_path)
    file_extension = file_path.suffix

    play_obj = None  # Initialize the play object

    # Handle WAV files with simpleaudio
    if file_extension == ".wav":
        def play_wav():
            nonlocal play_obj
            wave_obj = sa.WaveObject.from_wave_file(sound_path)
            play_obj = wave_obj.play()
            with active_sounds_lock:
                active_sounds.append(play_obj)  # Add the play object to active sounds

        # Run WAV playback in a separate thread
        threading.Thread(target=play_wav).start()

    # Handle MP3 files with pygame
    elif file_extension == ".mp3":
        def play_mp3():
            nonlocal play_obj
            if not pygame.mixer.get_init():
                pygame.mixer.init(Config.pygame_mixer['frequency'],
                   Config.pygame_mixer['size'],
                   Config.pygame_mixer['channels'],
                   Config.pygame_mixer['buffer'])

            sound = pygame.mixer.Sound(sound_path)  # Load the MP3 as a Sound object
            channel = sound.play()  # Play the sound on a new channel

            class PygamePlayObject:
                """Custom object to mimic active sound management for MP3s"""
                def __init__(self, channel, sound_path):
                    self.channel = channel
                    self.path = sound_path

                def is_playing(self):
                    return self.channel.get_busy()

                def stop(self):
                    if(self.channel is not None):
                        self.channel.stop()

            play_obj = PygamePlayObject(channel, sound_path)
            with active_sounds_lock:
                active_sounds.append(play_obj)  # Add the play object to active sounds

        # Run MP3 playback in a separate thread
        threading.Thread(target=play_mp3).start()

    else:
        print("Mais qu'est ce que t'as voulu lire: " + sound_path)

def stop():
    with active_sounds_lock:
        if(len(active_sounds) > 0):
            for sound in active_sounds:
                sound.stop()

            active_sounds.clear()
    
    if pygame.mixer.get_init():
        pygame.mixer.quit()

