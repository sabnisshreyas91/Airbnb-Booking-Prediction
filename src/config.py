from os import path

DEBUG = False
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 3000
APP_NAME = "penny-lane"
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/tracks.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "127.0.0.1"
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))
DATA_FOLDER = "data"
UNCOMPRESSED_DATA ="uncompressed_files"
ZIP_FILE_NAME = "AirBnb.zip"
