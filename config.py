import os

class Config:
    SAMPLES_PATH = "./samples/"    
    DEBUG = True
    # pygame mixer settings
    pygame_mixer = {
        'frequency': 44100,
        'size': -16,  # 16-bit signed
        'channels': 2,  # Stereo
        'buffer': 8192,  # Buffer size
    }