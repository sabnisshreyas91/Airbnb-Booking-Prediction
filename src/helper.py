import logging.config
import config
import os
import zipfile
import shutil

import boto3
from botocore.exceptions import ClientError
from zipfile import BadZipfile

logger = logging.getLogger(__name__)

# root = config.PROJECT_HOME
# data = config.DATA_FOLDER
# src_bucket_name = config.DATA_SOURCE_BUCKET_NAME
# root = config.PROJECT_HOME
# data = config.DATA_FOLDER
# uncompressed_data = config.UNCOMPRESSED_DATA
# zip_file_name = config.ZIP_FILE_NAME
# bucket_name = config.BUCKET_NAME
# bucket_folder = config.BUCKET_FOLDER
# logger.debug("Finished imports and reading in configs")

# destination_path = root+data+zip_file_name
# data_folder_path = root+data
# zip_file_path = data_folder_path+zip_file_name
# uncompressed_folder_path = data_folder_path+uncompressed_data


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


def unzip_file(uncompressed_folder_path, zip_file_name, zip_file_path):
    zip_folder_name = str.replace(zip_file_name, ".zip", "")+"//"
    shutil.rmtree(uncompressed_folder_path+zip_folder_name, ignore_errors=True)

    for file in os.listdir(uncompressed_folder_path):
        os.remove(os.path.join(uncompressed_folder_path, file))
        logger.warning("Deleted file %s as it already exists in %s", file, uncompressed_folder_path)

    logger.info("Commence extract of  '%s'", zip_file_name)
    try:
        zip_ref = zipfile.ZipFile(zip_file_path, 'r')
        zip_ref.extractall(uncompressed_folder_path)
    except FileNotFoundError as e:
        logger.error("File not found! Error: %s", e)
    except BadZipfile as e:
        logger.error("Zip file is corrupt. Error: %s", e)
    finally:
        zip_ref.close()
    logger.info("Extracted contents of '%s' to path '%s'", zip_file_name, uncompressed_folder_path)

    uncomp_folder = uncompressed_folder_path+zip_folder_name
    target_folder = uncompressed_folder_path

    logger.debug("Move extracted files to parent directory")
    for file in os.listdir(uncomp_folder):
        os.rename(uncomp_folder+file, target_folder+file)

    logger.debug("Delete empty directory '%s'", zip_folder_name)
    os.rmdir(uncomp_folder)


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


def load_data_to_S3(uncompressed_folder_path, bucket_name, bucket_folder):
    file_lst = os.listdir(uncompressed_folder_path)
    if len(file_lst) == 0:
        logger.warning("No Input files present in directory '%s', aborting operation", uncompressed_folder_path)
    else:
        for file in file_lst:
            fq_local_file_path = uncompressed_folder_path+file
            logger.info("Uploading file %s", fq_local_file_path)
            bucket_path = bucket_folder+file
            upload_file(fq_local_file_path, bucket_name, bucket_path)
            logger.info("Uploaded file %s", fq_local_file_path)