import os
DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 5000
APP_NAME = "airbnb-booking-prediction"
SQLALCHEMY_TRACK_MODIFICATIONS = False
HOST = "127.0.0.1"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100
RDS_FLAG = 'T' #set to 'T' to point to RDS instance. Any other value (eg: 'F') will point to local sqlite instance
MYSQL_DB = 'msia423'
MYSQL_PORT = '3306'
HOST = "127.0.0.1"
MAX_ROWS_SHOW=10
RDS_HOST = 'mysql-nw-shreyassabnis-msia423.ccuqnkdj9bb2.us-east-2.rds.amazonaws.com'
RDS_PORT = '3306'
USER = os.environ.get("MYSQL_USER")
PASSWORD = os.environ.get("MYSQL_PASSWORD")
CONN_TYPE ="mysql+pymysql"

if RDS_FLAG == 'T':
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".\
    format(CONN_TYPE, USER, PASSWORD, RDS_HOST, RDS_PORT, MYSQL_DB)
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/'+MYSQL_DB+".db"
