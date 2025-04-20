import os
from gtts import gTTS
from pathlib import Path
import pygame
import stat
import threading
import time
from app.fichiers import active_sounds_lock, active_sounds
from config import Config

# Initialize pygame mixer
pygame.mixer.init(Config.pygame_mixer['frequency'],
                   Config.pygame_mixer['size'],
                   Config.pygame_mixer['channels'],
                   Config.pygame_mixer['buffer'])

def speak(text, lang):

    if(Config.DEBUG):
        print("DEBUG: " + text)
        print("DEBUG: " + lang)
        
    try:
        # Generate speech
        tts = gTTS(text=text, lang=lang)
        timestamp = str(int(time.time()))
        filename = f"./figarot_{timestamp}.mp3"
        tts.save(filename)
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
        return

    def play_speech():
        if not pygame.mixer.get_init():
               pygame.mixer.init(Config.pygame_mixer['frequency'],
                   Config.pygame_mixer['size'],
                   Config.pygame_mixer['channels'],
                   Config.pygame_mixer['buffer'])
        
        sound = pygame.mixer.Sound(filename)
        channel = sound.play()

        class PygamePlayObject:
            """Custom object to manage active sound playback"""
            def __init__(self, channel, sound_path):
                self.channel = channel
                self.path = sound_path  # Store the file path

            def is_playing(self):
                return self.channel.get_busy()

            def stop(self):
                if self.channel is not None:
                    try:
                        self.channel.stop()
                        pygame.mixer.quit()  # Properly stop pygame audio
                    except Exception as e:
                        print(f"Error stopping sound: {e}")

                # Always delete the file when stopping
                self.delete_file()

            def delete_file(self):
                """Safely delete the MP3 file"""
                try:
                    os.remove(self.path)
                    print(f"Deleted file: {self.path}")
                except PermissionError:
                    os.chmod(self.path, stat.S_IWRITE)
                    os.remove(self.path)
                except FileNotFoundError:
                    pass  # File was already removed

        play_obj = PygamePlayObject(channel, filename)

        with active_sounds_lock:
            active_sounds.append(play_obj)

        # **Ensure the file is deleted after playing**
        while channel.get_busy():
            time.sleep(0.1)  # Wait while the sound is playing

        # When playback is finished, delete the file
        play_obj.delete_file()

        # Remove from active sounds list
        with active_sounds_lock:
            if play_obj in active_sounds:
                active_sounds.remove(play_obj)

        # Quit mixer only if no sounds are left
        with active_sounds_lock:
            if not active_sounds:
                pygame.mixer.quit()

    threading.Thread(target=play_speech, daemon=True).start()  # ✅ Daemonized to avoid hanging threads