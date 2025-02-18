from flask import Blueprint, render_template, request, send_file, jsonify
from app.fichiers import parse_directories, parse_files, play_audio_file, active_sounds, active_sounds_lock, stop
from app.voix import speak
from config import Config
import threading

main_bp = Blueprint('main', __name__)

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
        threading.Thread(target=play_audio_file, args=(sound_file,)).start()
        return jsonify({'status': 'playing', 'file': sound_file})
    
# Kill all sounds
@main_bp.route('/stop', methods=['POST'])
def stop_route():
    stop()
    return jsonify({"status": "stopped"})

# Text to speech
@main_bp.route('/speak', methods=['POST'])
def speak_route():
    data = request.json
    print("Received data:", data)  # Debugging print

    if not data:
        return jsonify({"status": "error", "message": "Invalid request"}), 400

    text = data.get("text", "")
    lang = data.get("lang", "en")

    if not text:
        return jsonify({"status": "error", "message": "No text provided"}), 400

    # Speak the text
    threading.Thread(target=speak, args=(text, lang)).start()

    return jsonify({"status": "success", "message": "Speaking text"})

