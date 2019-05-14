import logging
from botocore.exceptions import ClientError
import config
import os

import boto3

logger = logging.getLogger(__name__)

root = config.PROJECT_HOME
data = config.DATA_FOLDER
uncompressed_data = config.UNCOMPRESSED_DATA
bucket_name = config.BUCKET_NAME
bucket_folder = config.BUCKET_FOLDER
logger.debug("Finished imports and reading in configs")


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

file_lst = os.listdir(root+data+uncompressed_data)
for file in file_lst:
    fq_local_file_path = root+data+uncompressed_data+file
    logger.debug("Uploading file %s", fq_local_file_path)
    bucket_path = bucket_folder+file
    upload_file(fq_local_file_path, bucket_name, bucket_path)
    logger.debug("Uploaded file %s", fq_local_file_path)
