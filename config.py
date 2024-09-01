import os

class Config:
    SAMPLES_PATH = "./samples/"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = True
    # Add other configuration options as needed