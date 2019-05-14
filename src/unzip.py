import zipfile
import os
import config
import logging
from zipfile import BadZipfile

logger = logging.getLogger(__name__)


root = config.PROJECT_HOME
data = config.DATA_FOLDER
uncompressed_data = config.UNCOMPRESSED_DATA
zip_file_name = config.ZIP_FILE_NAME
logger.debug("Finished imports and reading in configs")

data_folder_path = root+"//"+data
zip_file_path = data_folder_path+"//"+zip_file_name
uncompressed_folder_path = data_folder_path+"//"+uncompressed_data

zip_folder_name = str.replace(zip_file_name, ".zip", "")

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

uncomp_folder = uncompressed_folder_path+"//"+zip_folder_name+"//"
target_folder = uncompressed_folder_path+"//"

logger.debug("Move extracted files to parent directory")
for file in os.listdir(uncomp_folder):
    os.rename(uncomp_folder+file, target_folder+file)

logger.debug("Delete empty directory '%s'", zip_folder_name)
os.rmdir(uncomp_folder)
