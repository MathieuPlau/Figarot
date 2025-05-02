from app import create_app
from audio.audio_engine import AudioEngine
from config import DEBUG, NETWORK
engine = AudioEngine()

app = create_app(audio_engine=engine)

if __name__ == "__main__":
    app.run(host=NETWORK["host"], port=NETWORK["port"], debug=DEBUG)