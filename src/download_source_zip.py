import logging.config
from botocore.exceptions import ClientError
import config
import os

import boto3

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

root = config.PROJECT_HOME
data = config.DATA_FOLDER
src_bucket_name = config.DATA_SOURCE_BUCKET_NAME
root = config.PROJECT_HOME
data = config.DATA_FOLDER
zip_file_name = config.ZIP_FILE_NAME
destination_path = root+data+zip_file_name

s3 = boto3.client('s3')

try:
    logger.info("Downloading %s from bucket %s", zip_file_name, src_bucket_name)
    s3.download_file(src_bucket_name, zip_file_name, root+data+zip_file_name)
    logger.info("Downloaded %s from bucket %s to %s", zip_file_name, src_bucket_name,destination_path)
except ClientError as e:
    if e.response['Error']['Code'] == "404":
        logger.warning("The object %s does not exist in AWS bucket %s.", zip_file_name, src_bucket_name)
    else:
        raise


def download_source_zip(src_bucket_name, zip_file_name, destination_path):
    s3 = boto3.client('s3')
    try:
        logger.info("Downloading %s from bucket %s", zip_file_name, src_bucket_name)
        s3.download_file(src_bucket_name, zip_file_name, root+data+zip_file_name)
        logger.info("Downloaded %s from bucket %s to %s", zip_file_name, src_bucket_name,destination_path)
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            logger.warning("The object %s does not exist in AWS bucket %s.", zip_file_name, src_bucket_name)
        else:
            raise
