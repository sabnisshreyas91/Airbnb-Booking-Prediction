from os import path

DEBUG = False
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 3000
APP_NAME = "airbnb-booking-prediction"
SQLALCHEMY_TRACK_MODIFICATIONS = True
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))+"//"
DATA_FOLDER = "data/"
UNCOMPRESSED_DATA = "uncompressed_files/"
ZIP_FILE_NAME = "AirBnb.zip"
DATA_SOURCE_BUCKET_NAME = "nw-shreyassabnis-msia423-public"
BUCKET_NAME = "nw-shreyassabnis-msia423"
BUCKET_FOLDER = "Input/"
MYSQL_DB = 'msia423'
MYSQL_PORT = '3306'
SQLITE_DATABASE_URI = 'sqlite:///'+DATA_FOLDER+MYSQL_DB
RDS_HOST = 'mysql-nw-shreyassabnis-msia423.ccuqnkdj9bb2.us-east-2.rds.amazonaws.com'
RDS_PORT = '3306'
RDS_FLAG = 'T' #set to 'T' to point to RDS instance. Any other value (eg: 'F') will point to local sqlite instance