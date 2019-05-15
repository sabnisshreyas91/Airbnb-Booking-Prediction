"""Enables the command line execution of multiple modules within src/

This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

Current commands enabled:

To create a database for Tracks with an initial song:

    `python run.py create --artist="Britney Spears" --title="Radar" --album="Circus"`

To add a song to an already created database:

    `python run.py ingest --artist="Britney Spears" --title="Radar" --album="Circus"`
"""
import logging.config
import src.config as config
# logging.config.fileConfig("config/logging/local.conf")
logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

from src.helper import download_source_zip, unzip_file, load_data_to_S3

root = config.PROJECT_HOME
data = config.DATA_FOLDER
src_bucket_name = config.DATA_SOURCE_BUCKET_NAME
root = config.PROJECT_HOME
data = config.DATA_FOLDER
uncompressed_data = config.UNCOMPRESSED_DATA
zip_file_name = config.ZIP_FILE_NAME
bucket_name = config.BUCKET_NAME
bucket_folder = config.BUCKET_FOLDER
logger.debug("Finished imports and reading in configs")

destination_path = root+data+zip_file_name
data_folder_path = root+data
zip_file_path = data_folder_path+zip_file_name
uncompressed_folder_path = data_folder_path+uncompressed_data


if __name__ == '__main__':
    download_source_zip(src_bucket_name, zip_file_name, destination_path)
    unzip_file(uncompressed_folder_path, zip_file_name, zip_file_path, )
    load_data_to_S3(uncompressed_folder_path, bucket_name, bucket_folder)
