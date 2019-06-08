import logging.config
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from xgboost.sklearn import XGBClassifier
from sklearn.model_selection import train_test_split
import scipy.stats as stats
import argparse

from numpy import loadtxt
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

import config
from helpers.helpers import read_csv_from_s3


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

vals = final_df.values
X = vals
le = LabelEncoder()
y = le.fit_transform(labels)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

xgb = XGBClassifier(max_depth=6, learning_rate=0.01, n_estimators=500,
                    objective='multi:softprob', subsample=0.5, colsample_bytree=0.5, seed=0,verbosity=1)                  
xgb.fit(X_train, y_train, verbose=True)