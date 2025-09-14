import os
import sys
import time
import json
import threading
import subprocess

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

def restart_app(detach: bool | None = None, delay_s: float = 0.2) -> None:
    """
    Restart the current Python program (Windows & Linux/macOS).

    - POSIX: in-place exec (cleanest).
    - Windows: spawn a detached child, then exit this one.
    - Safe to call from a background thread.
    """
    # Only the "real" Flask process should restart (not the reloader parent).
    # Values are: "true" for the reloader child, "false" for the parent, or None if no reloader.
    run_main = os.environ.get("WERKZEUG_RUN_MAIN")
    if run_main == "false":
        return  # ignore in the reloader parent

    if detach is None:
        detach = (os.name == "nt")  # default: detach on Windows

    python_or_exe = sys.executable
    argv = [python_or_exe] + sys.argv[1:]

    # POSIX: do a true in-place exec when not detaching
    if os.name == "posix" and not detach:
        os.execv(python_or_exe, [python_or_exe] + sys.argv)

    # Windows or forced-detach: spawn then exit
    creationflags = 0
    if os.name == "nt":
        # Detach so we don't inherit the current console/handles
        DETACHED_PROCESS = 0x00000008
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        if detach:
            creationflags |= (DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)

    subprocess.Popen([python_or_exe] + sys.argv, close_fds=True, creationflags=creationflags)
    time.sleep(delay_s)  # let the child start
    os._exit(0)


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

        # Restart after responding; daemon=True so it can't hang shutdown.
        threading.Thread(
            target=restart_app,
            kwargs={"detach": (os.name == "nt"), "delay_s": 0.2},
            daemon=True
        ).start()

        return "<h1>Figarot is rebooting…</h1><p>Please wait a moment and refresh the page.</p>"

    return render_template("settings.html", settings=settings)


