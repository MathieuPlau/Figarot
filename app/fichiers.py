import os
import simpleaudio as sa

# Function to parse the directory
def parse_directory(path):
    directory_contents = []
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            directory_contents.append({
                'type': 'folder',
                'name': dir_name,
                'path': dir_path
            })
        for file_name in files:
            file_path = os.path.join(root, file_name)
            directory_contents.append({
                'type': 'file',
                'name': file_name,
                'path': file_path
            })
    return directory_contents

def play_wave(sound):
    # Load the sound
    wave_obj = sa.WaveObject.from_wave_file(sound)  
    # Play the sound
    play_obj = wave_obj.play()
    # Wait for the sound to finish playing
    play_obj.wait_done()
