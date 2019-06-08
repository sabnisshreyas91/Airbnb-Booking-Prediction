from os import path

DEBUG = False
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 3000 #PORT = 9029
APP_NAME = "airbnb-booking-prediction"
SQLALCHEMY_TRACK_MODIFICATIONS = True
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))+"//"
DATA_FOLDER = "data/"
UNCOMPRESSED_DATA = "uncompressed_files/"
TRAIN_DATA = "train_users_2.csv"
SESSION_DATA = 'sessions.csv'
SESSIONS_FEATURE_COLUMNS = ['action', 'action_type', 'action_detail', 'device_type']
TRAIN_CATEGORICAL_COLUMNS = ['gender','signup_method','language','affiliate_channel','affiliate_provider','first_affiliate_tracked','signup_app','first_device_type','first_browser']
ZIP_FILE_NAME = "AirBnb.zip"
DATA_SOURCE_BUCKET_NAME = "nw-shreyassabnis-msia423-public"
DEFAULT_BUCKET_NAME = "nw-shreyassabnis-msia423"
DEFAULT_BUCKET_FOLDER = "Input/"
FEATURE_FOLDER = "features_labels/"
FEATURE_FILE_NAME = 'features.csv'
LABEL_FILE_NAME = 'label.csv'
TRAIN_FEATURE_FILE = 'X_train.csv'
TEST_FEATURE_FILE = 'X_test.csv'
TRAIN_LABEL_FILE = 'y_train.csv'
TEST_LABEL_FILE = 'y_test.csv'
TEST_SIZE = 0.20
SPLIT_RANDOM_STATE = 42
XG_MAX_DEPTH = 6
XG_LEARNING_RATE = 0.01
XG_N_ESTIMATORS = 500
XG_OBJECTIVE_FN = 'multi:softprob'
XG_SUBSAMPLE = 0.5
XG_COL_SAMPLE = 0.5
XG_SEED = 0
XG_FIT_VERBOSITY = 1
MODEL_S3_LOCATION = 'model/model.pkl'
MYSQL_DB = 'msia423.db'
MYSQL_PORT = '3306'
SQLITE_DATABASE_URI = 'sqlite:///'+DATA_FOLDER+MYSQL_DB
HOST = "127.0.0.1"
RDS_HOST = 'mysql-nw-shreyassabnis-msia423.ccuqnkdj9bb2.us-east-2.rds.amazonaws.com'
RDS_PORT = '3306'
RDS_FLAG = 'F' #set to 'T' to point to RDS instance. Any other value (eg: 'F') will point to local sqlite instance