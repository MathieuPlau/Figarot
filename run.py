from app import create_app
from audio.audio_engine import AudioEngine

engine = AudioEngine()

app = create_app(audio_engine=engine)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)