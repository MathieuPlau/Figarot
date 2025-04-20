import os
import stat
import time
import threading
from pathlib import Path
from gtts import gTTS
import simpleaudio as sa
import pygame

from config import Config


class AudioEngine:
    def __init__(self):
        pygame.mixer.init(**Config.pygame_mixer)
        self.active_sounds = []
        self.lock = threading.Lock()

    def _add_sound(self, sound_obj):
        with self.lock:
            self.active_sounds.append(sound_obj)

    def _remove_sound(self, sound_obj):
        with self.lock:
            if sound_obj in self.active_sounds:
                self.active_sounds.remove(sound_obj)

    def play_wav(self, file_path):
        def _play():
            if Config.DEBUG:
                print(f"[WAV] Playing {file_path}")
            wave_obj = sa.WaveObject.from_wave_file(file_path)
            play_obj = wave_obj.play()
            self._add_sound(play_obj)
            play_obj.wait_done()
            self._remove_sound(play_obj)

        threading.Thread(target=_play, daemon=True).start()

    def play_mp3(self, file_path):
        def _play():                
            if Config.DEBUG:
                print(f"[MP3] Playing {file_path}")
            if not pygame.mixer.get_init():
                pygame.mixer.init(**Config.pygame_mixer)

            sound = pygame.mixer.Sound(file_path)
            channel = sound.play()

            class PygameSoundWrapper:
                def __init__(self, channel):
                    self.channel = channel

                def stop(self):
                    if self.channel:
                        self.channel.stop()

            wrapper = PygameSoundWrapper(channel)
            self._add_sound(wrapper)

            while channel.get_busy():
                time.sleep(0.1)

            self._remove_sound(wrapper)

        threading.Thread(target=_play, daemon=True).start()

    def speak(self, text, lang='fr'):
        def _speak():
            try:
                tts = gTTS(text=text, lang=lang)
                filename = f"./figarot_{int(time.time())}.mp3"
                tts.save(filename)
            except Exception as e:
                print(f"[TTS Error] {e}")
                return

            sound = pygame.mixer.Sound(filename)
            channel = sound.play()

            class TTSWrapper:
                def __init__(self, channel, file_path):
                    self.channel = channel
                    self.file_path = file_path

                def stop(self):
                    if self.channel:
                        self.channel.stop()
                    self._cleanup()

                def _cleanup(self):
                    try:
                        os.remove(self.file_path)
                    except PermissionError:
                        os.chmod(self.file_path, stat.S_IWRITE)
                        os.remove(self.file_path)
                    except FileNotFoundError:
                        pass

            wrapper = TTSWrapper(channel, filename)
            self._add_sound(wrapper)

            while channel.get_busy():
                time.sleep(0.1)

            self._remove_sound(wrapper)
            wrapper._cleanup()

        threading.Thread(target=_speak, daemon=True).start()

    def play(self, file_or_text, lang='fr'):
        suffix = Path(file_or_text).suffix.lower()
        if suffix == '.wav':
            self.play_wav(file_or_text)
        elif suffix == '.mp3':
            self.play_mp3(file_or_text)
        else:
            self.speak(file_or_text, lang)

    def stop_all(self):
        with self.lock:
            for sound in self.active_sounds:
                try:
                    if Config.DEBUG:
                        print(f"[STOP] STFU !!!")
                    sound.stop()
                except Exception as e:
                    print(f"[Stop Error] {e}")
            self.active_sounds.clear()

        if pygame.mixer.get_init():
            pygame.mixer.stop()
