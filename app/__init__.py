from flask import Flask
from audio.audio_engine import AudioEngine
from .routes import main_bp

def create_app(audio_engine=None):
    app = Flask(__name__)
    
    # Load configurations
    app.config.from_object('config.Config')
    # Attach to app context
    app.audio_engine = audio_engine

    # Register Blueprints or routes    
    app.register_blueprint(main_bp)

    return app