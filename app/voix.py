import os
from gtts import gTTS
from pathlib import Path
import pygame
import stat
import threading
from config import Config

def speak(text, lang):

    if(Config.DEBUG):
        print("DEBUG: " + text)
        print("DEBUG: " + lang)
        
    """Convert text to speech and play it using pygame."""
    try:
        # Generate speech
        tts = gTTS(text=text, lang=lang)
        filename = "./figarot_tts.mp3"
        tts.save(filename)
        
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Unload the file from pygame before trying to delete it
        pygame.mixer.music.unload()  
        pygame.mixer.quit()  

        try:
            os.remove(filename)
        except PermissionError:            
            os.chmod(filename, stat.S_IWRITE)
            os.remove(filename)
        except FileNotFoundError:
        # File already gone
            pass

    except Exception as e:
        print(f"Error in text-to-speech: {e}")
