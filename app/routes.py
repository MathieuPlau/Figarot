from flask import Blueprint, render_template, request, send_file, jsonify
from app.fichiers import parse_directories, parse_files, play_wave
from config import Config
from pathlib import Path

main_bp = Blueprint('main', __name__)

@main_bp.route('/welcome')
def home():
    return render_template('home.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/')
def sounds():
    # Serve the main page with tabs for folders
    directory_path = request.args.get('dir', Config.SAMPLES_PATH)
    directory_contents = parse_directories(directory_path)  # Get only directories
    return render_template('sounds.html', directory_contents=directory_contents, directory_path=directory_path)

@main_bp.route('/folder_contents')
def folder_contents():
    # Fetch the contents of a folder dynamically
    folder_path = request.args.get('folder')
    folder_contents = parse_files(Config.SAMPLES_PATH + folder_path)  # Get only files in the folder
    return jsonify(folder_contents)

# Play a given sound
@main_bp.route('/play_sound', methods=['POST'])
def play_sound():    
    sound_file = request.json.get('file_path')  # Get the file path from the request
    if sound_file:        
        play_wave(sound_file)
        return jsonify({'status': 'success', 'message': f'Playing sound: {sound_file}'})
    else:
        return jsonify({'status': 'error', 'message': 'No file specified'}), 400
