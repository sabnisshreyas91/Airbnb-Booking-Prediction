"""Enables the command line execution of multiple modules within src/

Current commands enabled:

To pull data from the source (a public bucket) on to the local file system, unzip data and then push to
a configurable target S3 bucket.

    `python run.py`
"""
import logging.config
import src.config as config
import os
import argparse
#from app.app import app
#logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

from src.data_ingest_schema_create import download_source_zip, unzip_file, load_data_to_S3, create_schema

root = config.PROJECT_HOME
data = config.DATA_FOLDER
src_bucket_name = config.DATA_SOURCE_BUCKET_NAME
root = config.PROJECT_HOME
data = config.DATA_FOLDER
uncompressed_data = config.UNCOMPRESSED_DATA
zip_file_name = config.ZIP_FILE_NAME
bucket_name = config.DEFAULT_BUCKET_NAME
bucket_folder = config.DEFAULT_BUCKET_FOLDER

parser = argparse.ArgumentParser()
parser.add_argument("--bucket_name", default= bucket_name, help="S3 bucket to upload the source data to. Default:nw-shreyassabnis-msia423")
parser.add_argument("--bucket_folder", default= bucket_folder, help="Folder within S3 bucket where wd'd like the data to be uploaded. Default:Input/")
#parser.add_argument("--app", default= 'F', help="Folder within S3 bucket where wd'd like the data to be uploaded. Default:Input/")
args = parser.parse_args()

user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = config.RDS_HOST
port = config.RDS_PORT
databasename = config.MYSQL_DB
# Indicator to decide if RDBMS schema should be created in local sqlite vs AWS RDS
rds_flag = config.RDS_FLAG
sqlite_uri = config.SQLITE_DATABASE_URI
logger.debug("Finished imports and reading in configs")


destination_path = root+data+zip_file_name
data_folder_path = root+data
# The folder to which the source .zip file from the public source bucket will be downloaded to
zip_file_path = data_folder_path+zip_file_name
# Location where the zip files will be extracted to
uncompressed_folder_path = data_folder_path+uncompressed_data


if __name__ == '__main__':
    download_source_zip(src_bucket_name, zip_file_name, destination_path)
    unzip_file(uncompressed_folder_path, zip_file_name, zip_file_path )
    load_data_to_S3(uncompressed_folder_path, args.bucket_name, args.bucket_folder)
    create_schema(user, password, host, port, databasename, sqlite_uri, rds_flag)
    # if(args.app == 'T'):
    #     app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])

