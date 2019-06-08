import logging.config
import config
import os
import zipfile
import shutil

import boto3
from botocore.exceptions import ClientError
from zipfile import BadZipfile
import sqlalchemy as sql

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, Date
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


def download_source_zip(src_bucket_name, zip_file_name, destination_path):
    """
    Downloads compressed data from source public bucket (config.DATA_SOURCE_BUCKET_NAME)
    to a folder in the local filesystem.
    
    :param src_bucket_name: Name of the source public bucket
    :param zip_file_name: Name of the .zip file in the source bucket.
    :param destination_path: Fully qualified path of folder where the .zip file will be extracted

    :return: None
    """
    s3 = boto3.client('s3')
    try:
        logger.info("Downloading %s from bucket %s", zip_file_name, src_bucket_name)
        s3.download_file(src_bucket_name, zip_file_name, destination_path)
        logger.info("Downloaded %s from bucket %s to %s", zip_file_name, src_bucket_name,destination_path)
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            logger.warning("The object %s does not exist in AWS bucket %s.", zip_file_name, src_bucket_name)
        else:
            raise


def unzip_file(uncompressed_folder_path, zip_file_name, zip_file_path):
    """
    Unzips source file into destination folder
    
    :param uncompressed_folder_path: Destination folder to which the uncompressed files will be sent
    :param zip_file_name: Name of the .zip file in the local filesystem
    :param zip_file_path: Fully qualified path of folder where the .zip file resides.

    :return: None
    """
    zip_folder_name = str.replace(zip_file_name, ".zip", "")+"//"
    # Deletes airbnb/ folder if it exists inside the uncompressed folder, this can happen due to an interrupted run
    shutil.rmtree(uncompressed_folder_path+zip_folder_name, ignore_errors=True)

    # Create uncompressed/ folder if it does not exist
    if(os.path.exists(uncompressed_folder_path) == False):
        os.mkdir(uncompressed_folder_path)

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
    """
    Upload a file to an S3 bucket

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
    """
    Uploads extracted source data files to a specific folder in an S3 bucket
    
    :param uncompressed_folder_path: Location of unzipped files in local filesystem
    :param bucket_name: Bucket to upload to
    :param bucket_folder: Subfolder within S3 bucket to upload to

    :return: None
    """
    file_lst = os.listdir(uncompressed_folder_path)
    if len(file_lst) == 0:
        logger.warning("No Input files present in directory '%s', aborting operation", uncompressed_folder_path)
    else:
        logger.info("\nUploading to destination bucket %s\n",bucket_name)
        for file in file_lst:
            if file == 'sessions.csv':
                continue
            else:
                fq_local_file_path = uncompressed_folder_path+file
                logger.info("Uploading file %s to bucket %s", fq_local_file_path, bucket_name)
                bucket_path = bucket_folder+file
                upload_file(fq_local_file_path, bucket_name, bucket_path)
                logger.info("Uploaded file %s to bucket %s", fq_local_file_path, bucket_name)


def create_db(engine=None, engine_string=None):
    """
    Creates a database with the data models inherited from `Base` (Tweet and TweetScore).

    
        :param engine: SQLAlchemy connection engine. If None, `engine_string` must be provided.
        :param engine_string: String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.

    Returns:
        None
    """
    if engine is None and engine_string is None:
        return ValueError("`engine` or `engine_string` must be provided")
    elif engine is None:
        engine = sql.create_engine(engine_string)


def create_schema(user, password, host, port, databasename, sqlite_uri, rds_flag):
    """
    Creates data models of tables to create in destination database and calls function to
    create the tables in destination database

        :param user: username for the destination AWS RDS database. Obtained as environment variable in run.py
        :param password: password for the user parameter. Obtained as environment variable in run.py
        :param host: Host (endpoint) of the AWS RDS database.
        :param port: Connection of the AWS RDS database
        :param databasename: Name of the database that will be created in either AWS RDS or sqlite. Default: msia423 
        :param sqlite_uri: local path where the sqlite database should be created
        :rds_flag: T-> create schema in RDS instance. F-> create schema in local sqlite database.
    """
    Base = declarative_base()
    if rds_flag == 'T':
        logger.info("\ngenerating schema for '%s' database in AWS RDS\n", databasename)
        conn_type = "mysql+pymysql"
        engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, databasename)
        engine = sql.create_engine(engine_string)
    else:
        logger.info("\ngenerating schema for '%s' database in sqlite\n",databasename)
        engine = sql.create_engine(sqlite_uri)
        create_db(engine_string=sqlite_uri)

    class UserInput(Base):
        """Create a data model to store any user inputs to the app """
        __tablename__ = 'User_Input'
        id = Column(Integer, primary_key=True)
        Age = Column(Integer, unique=False, nullable=False)
        Gender = Column(String(100), unique=False, nullable=False)
        SignupMethod = Column(String(100), unique=False, nullable=False)
        Language = Column(String(100), unique=False, nullable=False)
        DateAccountCreated = Column(Date, unique=False, nullable=False)

    def __repr__(self):
        return '<UserInput %r>' % self.title
        
    Base.metadata.create_all(engine)
