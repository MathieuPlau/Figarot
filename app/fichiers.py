import os
import simpleaudio as sa

# Returns directories from the given path
def parse_directories(path):
    directories = []
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_dir():
                directories.append({
                    'name': entry.name,
                    'type': 'folder'
                })
    return directories 

# Returns files from the given directory
def parse_files(directory_path): 
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

def play_wave(sound):
    # Load the sound
    wave_obj = sa.WaveObject.from_wave_file(sound)  
    # Play the sound
    play_obj = wave_obj.play()
    # Wait for the sound to finish playing
    play_obj.wait_done()
