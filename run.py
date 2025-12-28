from app import create_app
from audio.audio_engine import AudioEngine
# On ajoute l'import de la config ici
from config import Config 

engine = AudioEngine()
app = create_app(audio_engine=engine)

if __name__ == "__main__":
    app.run(
        host=Config.NETWORK["host"], 
        port=Config.NETWORK["port"], 
        debug=Config.DEBUG
    )