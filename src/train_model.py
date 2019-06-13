import logging.config
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from xgboost.sklearn import XGBClassifier
from sklearn.model_selection import train_test_split
import scipy.stats as stats
import argparse
import io
import pickle 
import boto3

from numpy import loadtxt
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

import config
from helpers.helpers import read_csv_from_s3

log_file_path = config.LOGGING_CONFIG
logging.config.fileConfig(log_file_path)

logger = logging.getLogger(__name__)

bucket_name = config.DEFAULT_BUCKET_NAME
bucket_folder = config.FEATURE_FOLDER
X_train_fname = config.TRAIN_FEATURE_FILE
y_train_fname = config.TRAIN_LABEL_FILE

parser = argparse.ArgumentParser()
parser.add_argument("--bucket_name", default=bucket_name, help="S3 bucket to upload the source data to. Default:nw-shreyassabnis-msia423")
parser.add_argument("--bucket_folder", default=bucket_folder, help="Folder within S3 bucket where wd'd like the data to be uploaded. Default:Input/")
args = parser.parse_args()

X_train = read_csv_from_s3(args.bucket_name, args.bucket_folder, X_train_fname)
logger.info("Read %s from bucket %s", X_train_fname, args.bucket_name)
y_train = read_csv_from_s3(args.bucket_name, args.bucket_folder, y_train_fname)
logger.info("Read %s from bucket %s", y_train_fname, args.bucket_name)

xgb = XGBClassifier(max_depth=config.XG_MAX_DEPTH
                   ,learning_rate=config.XG_LEARNING_RATE
                   ,n_estimators=config.XG_N_ESTIMATORS
                   ,objective=config.XG_OBJECTIVE_FN
                   ,subsample=config.XG_SUBSAMPLE
                   ,colsample_bytree=config.XG_COL_SAMPLE
                   ,seed=config.XG_SEED
                   ,verbosity=config.XG_FIT_VERBOSITY)      
logger.debug("Initialized model")

logger.info("Started model training")
xgb.fit(X_train.values, y_train.values, verbose=config.XG_FIT_VERBOSITY)
logger.info("Model training complete")
pickle_buffer = io.BytesIO()
s3_resource = boto3.resource('s3')
pickle.dump(xgb, pickle_buffer)
s3_resource.Object(args.bucket_name, config.MODEL_S3_LOCATION).put(Body=pickle_buffer.getvalue())
logger.info("Saved pickled model to %s in bucket %s",config.MODEL_S3_LOCATION,args.bucket_name)