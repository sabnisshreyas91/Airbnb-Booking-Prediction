from os import path

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 3000
APP_NAME = "penny-lane"
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/tracks.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "127.0.0.1"
DATA = "data"
# Getting the parent directory of this file. That will function as the project home.
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))