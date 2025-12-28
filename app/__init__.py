import os
from flask import Flask, render_template, send_from_directory, jsonify, request
from config import Config

def create_app(audio_engine=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route('/')
    def index():
        base_path = app.config['SAMPLES_PATH']
        contents = []
        if os.path.exists(base_path):
            for name in os.listdir(base_path):
                if os.path.isdir(os.path.join(base_path, name)):
                    contents.append({'name': name, 'type': 'folder'})
        return render_template('sounds.html', directory_contents=contents)

    @app.route('/folder_contents')
    def folder_contents():
        folder = request.args.get('folder')
        folder_path = os.path.join(app.config['SAMPLES_PATH'], folder)
        files = []
        if os.path.exists(folder_path):
            for f in os.listdir(folder_path):
                if f.lower().endswith(('.wav', '.mp3')):
                    files.append({'name': f, 'type': 'file'})
        return jsonify(files)

    # LA ROUTE CORRIGÉE
    @app.route('/audio/<path:filename>')
    def serve_audio(filename):
        # On récupère le chemin absolu du dossier de sons
        base_path = os.path.abspath(app.config['SAMPLES_PATH'])
        
        # DEBUG : Affiche dans ton terminal pour vérifier le chemin
        print(f"--- LECTURE AUDIO ---")
        print(f"Recherche dans : {base_path}")
        print(f"Fichier : {filename}")
        
        # send_from_directory gère automatiquement la sécurité et les espaces
        return send_from_directory(base_path, filename)

    return app