import os
from config import Config
from pathlib import Path

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