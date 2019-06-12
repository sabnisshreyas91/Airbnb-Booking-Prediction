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
from io import BytesIO, StringIO

import config
from helpers.helpers import read_csv_from_s3, read_array_from_s3, write_csv_to_s3


log_file_path = config.LOGGING_CONFIG#"../"+config.LOGGING_CONFIG
logging.config.fileConfig(log_file_path)

logger = logging.getLogger(__name__)

bucket_name = config.DEFAULT_BUCKET_NAME
bucket_folder = config.FEATURE_FOLDER
X_test_fname = config.TEST_FEATURE_FILE
y_test_fname = config.TEST_LABEL_FILE

parser = argparse.ArgumentParser()
parser.add_argument("--bucket_name", default=bucket_name, help="S3 bucket to upload the source data to. Default:nw-shreyassabnis-msia423")
parser.add_argument("--bucket_folder", default=bucket_folder, help="Folder within S3 bucket where wd'd like the data to be uploaded. Default:Input/")
args = parser.parse_args()


X_test = read_csv_from_s3(args.bucket_name, args.bucket_folder, X_test_fname)
logger.info("Read %s from bucket %s", X_test_fname, args.bucket_name)
y_test = read_csv_from_s3(args.bucket_name, args.bucket_folder, y_test_fname)
logger.info("Read %s from bucket %s", y_test_fname, args.bucket_name)
labels = read_csv_from_s3(args.bucket_name, config.FEATURE_FOLDER, config.LABEL_FILE_NAME)
logger.info("Read %s from bucket %s", config.LABEL_FILE_NAME, args.bucket_name)
le = LabelEncoder()
y = le.fit_transform(labels)
logger.info("read test feature file %s and test label file %s from bucket %s and folder %s",X_test_fname, y_test_fname, args.bucket_name, args.bucket_folder)

s3 = boto3.resource('s3')
with BytesIO() as data:
    s3.Bucket(args.bucket_name).download_fileobj(config.MODEL_S3_LOCATION, data)
    data.seek(0)    # move back to the beginniaaang aftezsassxdsssr writing
    model = pickle.load(data)
logger.info("Loaded saved model %s from bucket %s",config.MODEL_S3_LOCATION , args.bucket_name)

prediction = model.predict_proba(X_test.values)
y_pred_names = []
for i in range(len(prediction)):
    y_pred_names.append(list(le.inverse_transform(np.argsort(prediction[i])[::-1])[:2]))


pred_ver = []
for i,val in enumerate(list(le.inverse_transform(y_test))):
    if val in y_pred_names[i]:
        pred_ver.append(1)
    else:
        pred_ver.append(0)

top_2_accuracy = round(sum(pred_ver)/len(pred_ver),2)
predictions = pd.DataFrame(y_pred_names, columns = ['country_pred_1','country_pred_2'])

write_csv_to_s3(pd.DataFrame(predictions,columns = list(predictions)), args.bucket_name, args.bucket_folder, config.PREDICTION_FILE)
logger.info("wrote predictions to %s", config.MODEL_FOLDER + config.PREDICTION_FILE)


write_string= 'model: '+str(model)+'\n'
write_string+='test file: '+y_test_fname+'\n'
write_string+='features used: '+str(config.TRAIN_CATEGORICAL_COLUMNS+config.SESSIONS_FEATURE_COLUMNS)
write_string+='\nAccuracy on test:' + str(top_2_accuracy)
print(write_string)

output = StringIO()
output.write(write_string)

s3_resource = boto3.resource('s3')
s3_resource.Object(args.bucket_name, config.MODEL_FOLDER+config.METRICS_FILE).put(Body=output.getvalue())