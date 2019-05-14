import logging.config
from botocore.exceptions import ClientError
import config
import os

import boto3

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

src_bucket_name = config.DATA_SOURCE_BUCKET_NAME
root = config.PROJECT_HOME
data = config.DATA_FOLDER

s3 = boto3.resource('s3')

try:
    #s3.Bucket(BUCKET_NAME).download_file(KEY, 'my_local_image.jpg')
    s3.download_file(src_bucket_name, 'AirBnB.zip', 'AirBnB.zip')
except ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise
