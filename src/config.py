from os import path

DEBUG = False
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 3000
APP_NAME = "airbnb-booking-prediction"
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/tracks.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "127.0.0.1"
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))+"//"
DATA_FOLDER = "data/"
UNCOMPRESSED_DATA = "uncompressed_files/"
ZIP_FILE_NAME = "AirBnb.zip"
DATA_SOURCE_BUCKET_NAME = "nw-shreyassabnis-msia423-public"
BUCKET_NAME = "nw-shreyassabnis-msia423"
BUCKET_FOLDER = "Input/"
MYSQL_DB = 'msia423'
MYSQL_PORT = '3306'