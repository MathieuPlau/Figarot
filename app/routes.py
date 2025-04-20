from flask import Blueprint, render_template, request, send_file, jsonify, current_app
from audio.audio_engine import AudioEngine
from app.fichiers import parse_directories, parse_files, play_audio_file, active_sounds, active_sounds_lock, stop
from app.voix import speak
from config import Config
import threading
import os

main_bp = Blueprint('main', __name__)
audio_engine = AudioEngine()

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
   
# Kill all sounds
@main_bp.route('/stop', methods=['POST'])
def stop_sounds():
    audio_engine.stop_all()
    return jsonify({'status': 'stopped'}), 200

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

@main_bp.route("/play_sound", methods=["POST"])
def play_sound():
    data = request.get_json()
    file_path = data.get('file_path')

    if(Config.DEBUG):
        print("Received file path:", file_path)

    if not file_path:
        return jsonify({'status': 'error', 'message': 'No file path provided'}), 400

    # Choose how to play based on extension
    _, ext = os.path.splitext(file_path.lower())
    try:
        if ext == '.wav':
            audio_engine.play_wav(file_path)  # Ensure audio_engine is properly initialized
        elif ext == '.mp3':
            audio_engine.play_mp3(file_path)
        else:
            return jsonify({'status': 'error', 'message': 'Unsupported file type'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({'status': 'success', 'message': f'Playing {file_path}'}), 200


