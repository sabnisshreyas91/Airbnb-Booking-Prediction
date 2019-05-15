"""Enables the command line execution of multiple modules within src/

Current commands enabled:

To pull data from the source (a public bucket) on to the local file system, unzip data and then push to
a configurable target S3 bucket.

    `python run.py`
"""
import logging.config
import src.config as config
import os

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

from src.helper import download_source_zip, unzip_file, load_data_to_S3, create_schema

root = config.PROJECT_HOME
data = config.DATA_FOLDER
src_bucket_name = config.DATA_SOURCE_BUCKET_NAME
root = config.PROJECT_HOME
data = config.DATA_FOLDER
uncompressed_data = config.UNCOMPRESSED_DATA
zip_file_name = config.ZIP_FILE_NAME
bucket_name = config.BUCKET_NAME
bucket_folder = config.BUCKET_FOLDER

user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = config.RDS_HOST
port = config.RDS_PORT
databasename = config.MYSQL_DB
rds_flag = config.RDS_FLAG
sqlite_uri = config.SQLITE_DATABASE_URI
logger.debug("Finished imports and reading in configs")


destination_path = root+data+zip_file_name
data_folder_path = root+data
zip_file_path = data_folder_path+zip_file_name
uncompressed_folder_path = data_folder_path+uncompressed_data


if __name__ == '__main__':
    download_source_zip(src_bucket_name, zip_file_name, destination_path)
    unzip_file(uncompressed_folder_path, zip_file_name, zip_file_path, )
    load_data_to_S3(uncompressed_folder_path, bucket_name, bucket_folder)
    create_schema(user, password, host, port, databasename, sqlite_uri, rds_flag)
