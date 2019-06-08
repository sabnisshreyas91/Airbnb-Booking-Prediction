import logging.config
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import scipy.stats as stats
import argparse

from numpy import loadtxt


import config
from helpers.helpers import read_csv_from_s3, write_csv_to_s3


log_file_path = "../"+config.LOGGING_CONFIG
logging.config.fileConfig(log_file_path)

logger = logging.getLogger(__name__)

bucket_name = config.DEFAULT_BUCKET_NAME
bucket_folder = config.FEATURE_FOLDER
features = config.FEATURE_FILE_NAME
labels = config.LABEL_FILE_NAME

parser = argparse.ArgumentParser()
parser.add_argument("--bucket_name", default=bucket_name, help="S3 bucket to upload the source data to. Default:nw-shreyassabnis-msia423")
parser.add_argument("--bucket_folder", default=bucket_folder, help="Folder within S3 bucket where wd'd like the data to be uploaded. Default:Input/")
args = parser.parse_args()

feature_df = read_csv_from_s3(args.bucket_name, args.bucket_folder, features)
label_df = read_csv_from_s3(args.bucket_name, args.bucket_folder, labels)

X = feature_df.values
le = LabelEncoder()
y = le.fit_transform(label_df)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=config.TEST_SIZE, random_state=config.SPLIT_RANDOM_STATE)
logger.info("split training features and labels into %.1f train and %.1f test", (1-config.TEST_SIZE), config.TEST_SIZE)

write_csv_to_s3(X_train, args.bucket_name, args.bucket_folder, 'X_train.csv', arr=True)
logger.info("wrote training features to %s", config.FEATURE_FOLDER + config.TRAIN_FEATURE_FILE)
write_csv_to_s3(X_test, args.bucket_name, args.bucket_folder, 'X_test.csv', arr=True)
logger.info("wrote testing features to %s", config.FEATURE_FOLDER + config.TEST_FEATURE_FILE)
write_csv_to_s3(y_train, args.bucket_name, args.bucket_folder, 'y_train.csv', arr=True)
logger.info("wrote training labels to %s", config.FEATURE_FOLDER + config.TRAIN_LABEL_FILE)
write_csv_to_s3(y_test, args.bucket_name, args.bucket_folder, 'y_test.csv', arr=True)
logger.info("wrote testing labels to %s", config.FEATURE_FOLDER + config.TEST_LABEL_FILE)