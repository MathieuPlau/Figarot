from flask import Blueprint, render_template, request, send_file, jsonify
from app.fichiers import parse_directory, play_wave
from config import Config
from pathlib import Path

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/sounds')
def sounds():
    directory_path = request.args.get('dir', Config.SAMPLES_PATH)  # default to current directory
    directory_contents = parse_directory(directory_path)
    return render_template('sounds.html', directory_contents=directory_contents, directory_path=directory_path)

# @main_bp.route('/wav')
# def soundtest():
#     sound_path = Path(Config.SAMPLES_PATH) / "Bobo.wav"

#     if sound_path.exists():
#         try:
#             play_wave(str(sound_path))  # Play sound on the server
#             return jsonify({"status": "success", "message": "Sound played successfully"})
#         except Exception as e:
#             return jsonify({"status": "error", "message": str(e)}), 500
#     else:
#         return jsonify({"status": "error", "message": "File not found"}), 404

@main_bp.route('/wav')
def soundtest():
    sound_path = Path(Config.SAMPLES_PATH) / "Bobo.wav"
    return play_wave(str(sound_path))
