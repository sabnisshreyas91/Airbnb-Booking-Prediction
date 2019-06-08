import logging.config
import os
from os import path
import pandas as pd
import config
import argparse
import numpy as np
from helpers.helpers import read_csv_from_s3, write_csv_to_s3
from io import StringIO
import boto3

log_file_path = "../"+config.LOGGING_CONFIG
logging.config.fileConfig(log_file_path)

logger = logging.getLogger(__name__)

bucket_name = config.DEFAULT_BUCKET_NAME
bucket_folder = config.DEFAULT_BUCKET_FOLDER
train_data = config.TRAIN_DATA
session_data = config.SESSION_DATA


parser = argparse.ArgumentParser()
parser.add_argument("--bucket_name", default=bucket_name, help="S3 bucket to upload the source data to. Default:nw-shreyassabnis-msia423")
parser.add_argument("--bucket_folder", default=bucket_folder, help="Folder within S3 bucket where wd'd like the data to be uploaded. Default:Input/")
args = parser.parse_args()


def get_session_features(df, column):
    df['count'] = 1
    ret_df = df[['user_id', column, 'count']].fillna(-1)\
                                             .groupby(['user_id', column])\
                                             .count().reset_index()\
                                             .pivot(index='user_id', columns= column, values='count')\
                                             .fillna(0)
    return ret_df

logger.info("Reading %s from bucket %s", train_data, args.bucket_name)
df_train = read_csv_from_s3(args.bucket_name, args.bucket_folder, train_data)
logger.info("Read %s from bucket %s", train_data, args.bucket_name)
logger.info("Reading %s from bucket %s", session_data, args.bucket_name)
df_sess = read_csv_from_s3(args.bucket_name, args.bucket_folder, session_data)
logger.info("Read %s from bucket %s", session_data, args.bucket_name)


df_train = df_train[(df_train.country_destination!='NDF') & (df_train.country_destination!='other') & ((df_train.country_destination!='US'))]
logger.info("Filtered NDF, other, and US data from training data")
df_train_user_id = df_train[['id']]
df_sess = df_sess.merge(df_train_user_id, how='inner', left_on='user_id', right_on='id')
logger.info("Filtered sessions to only include user_id's that exist in training data")
df_sess.drop('id', axis=1, inplace=True)
df_sess_user_id = df_sess[['user_id']].drop_duplicates()
df_train = df_train.merge(df_sess_user_id, how='inner', left_on='id', right_on='user_id')
logger.info("Filtered df_train to only include user_id's that exist in session data")
df_labels = df_train[['country_destination']]
logger.info("Saved labels into dataframe")
df_train = df_train.drop(['country_destination'], axis=1)
logger.debug("dropped label from training data")

df_sess_features = df_sess.fillna(-1).groupby('user_id').agg({'secs_elapsed': [np.mean, np.std, np.median]})
logger.info("Created seconds elapsed features")

col_lst = config.SESSIONS_FEATURE_COLUMNS
for col in col_lst:
    df = get_session_features(df_sess, col)
    df_sess_features = df_sess_features.merge(df, left_index=True, right_index=True, how='inner')
    logger.info("Created features for column:%s", col)

df_train.set_index('id', inplace=True)
train_dummy = pd.get_dummies(df_train[config.TRAIN_CATEGORICAL_COLUMNS])
logger.info("Obtained dummy categorical features")

final_df = train_dummy.merge(df_sess_features, left_index=True, right_index=True, how='inner')
logger.info("Combined to get final_df")

write_csv_to_s3(final_df, args.bucket_name, config.FEATURE_FOLDER, config.FEATURE_FILE_NAME)
logger.info("wrote features to %s", config.FEATURE_FOLDER + config.FEATURE_FILE_NAME)

write_csv_to_s3(df_labels, args.bucket_name, config.FEATURE_FOLDER, config.LABEL_FILE_NAME)
logger.info("wrote labels to %s", config.FEATURE_FOLDER + config.LABEL_FILE_NAME)
