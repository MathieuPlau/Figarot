import json
import threading
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from audio.audio_engine import AudioEngine
from app.file_manager import parse_directories, parse_files
from config import SAMPLES_PATH, DEBUG, CONFIG_FILE

main_bp = Blueprint('main', __name__)
audio_engine = AudioEngine()

@main_bp.route('/')
def sounds():
    # Serve the main page with tabs for folders
    directory_path = request.args.get('dir', SAMPLES_PATH)
    directory_contents = parse_directories(directory_path)  # Get only directories
    return render_template('sounds.html', directory_contents=directory_contents, directory_path=directory_path)

@main_bp.route('/folder_contents')
def folder_contents():
    # Fetch the contents of a folder dynamically
    folder_path = request.args.get('folder')
    folder_contents = parse_files(SAMPLES_PATH + folder_path)  # Get only files in the folder
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

    if(DEBUG):
        print("Received data:", data)  # Debugging print

    if not data:
        return jsonify({"status": "error", "message": "Invalid request"}), 400

    text = data.get("text", "")
    lang = data.get("lang", "")

    if not text:
        return jsonify({"status": "error", "message": "No text provided"}), 400

    # Speak the text
    audio_engine.play(text, lang)

    return jsonify({'status': 'success', 'message': f'Speaking {text, lang}'}), 200

# Sounds !
@main_bp.route("/play_sound", methods=["POST"])
def play_sound():
    data = request.get_json()
    file_path = data.get('file_path')

    if(DEBUG):
        print("Received file path:", file_path)

    if not file_path:
        return jsonify({'status': 'error', 'message': 'No file path provided'}), 400

    try:
        audio_engine.play(file_path)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({'status': 'success', 'message': f'Playing {file_path}'}), 200

def restart_app():
    """Replaces the current process with a new one using the same command line."""
    python = sys.executable
    os.execv(python, [python] + sys.argv)

def load_settings():
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

def save_settings(settings):
    with open(CONFIG_FILE, "w") as file:
        json.dump(settings, file, indent=4)

@main_bp.route("/settings", methods=["GET", "POST"])
def settings_page():
    settings = load_settings()

    if request.method == "POST":
        settings["samples_path"] = request.form.get("samples_path", "")
        settings["chaos_mode"] = "chaos_mode" in request.form
        settings["debug"] = "debug" in request.form

        # Audio settings
        volume = request.form.get("volume")
        if volume is not None:
            settings.setdefault("audio_settings", {})
            settings["audio_settings"]["volume"] = int(volume)

        # Network settings
        settings.setdefault("network", {})
        settings["network"]["host"] = request.form.get("network_host", "0.0.0.0")
        settings["network"]["port"] = int(request.form.get("network_port", 5000))

        # Pygame mixer settings
        settings.setdefault("pygame_mixer", {})
        settings["pygame_mixer"]["frequency"] = int(request.form.get("frequency", 44100))
        settings["pygame_mixer"]["size"] = int(request.form.get("size", -16))
        settings["pygame_mixer"]["channels"] = int(request.form.get("channels", 2))
        settings["pygame_mixer"]["buffer"] = int(request.form.get("buffer", 8192))

        save_settings(settings)
        threading.Thread(target=restart_app).start()
        return "<h1>Figarot is rebooting…</h1><p>Please wait a moment and refresh the page.</p>"


    return render_template("settings.html", settings=settings)


