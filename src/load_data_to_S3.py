import boto3
from botocore.exceptions import ClientError
import os
import logging.config

root = "D:\\Northwestern\\MSiA\\SQ 2019\\AVC\\Project\\Ideas\\Airbnb-Booking-Prediction\\"
data = "\\data"
uncompressed_data ="\\uncompressed_files"
bucket_name = "nw-shreyassabnis-msia423"
bucket_folder = "input2/"

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
    local_path = root+data+uncompressed_data+"\\"+file
    bucket_path = bucket_folder+file
    if(file == "sessions.csv"):
        continue
    else:
        #print(local_path,bucket_path)
        #print("---")
        print(file,'started')
        upload_file(local_path,bucket_name,bucket_path)
        print(file,'ended')
    
#upload_file("D:\\Northwestern\\MSiA\\SQ 2019\\AVC\\Project\\Ideas\\Airbnb-Booking-Prediction\\data\\uncompressed_files\\countries.csv","nw-shreyassabnis-msia423","input/countries.csv")
#upload_file("D:\\Northwestern\\MSiA\\SQ 2019\\AVC\\Project\\Ideas\\Airbnb-Booking-Prediction\\data\\uncompressed_files\\countries.csv","nw-shreyassabnis-msia423","input/countries.csv")