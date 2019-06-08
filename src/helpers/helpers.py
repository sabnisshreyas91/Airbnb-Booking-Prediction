import numpy as np
import datetime
import pandas as pd
import boto3
from botocore.exceptions import ClientError
from io import StringIO
import boto3

class Timer:
    """Times the code within the with statement and logs the elapsed time when it closes.

           Args:
               function (string): Name of function being timed
               logger (obj:`logging.logger`): Logger to have elapsed time logged to
   """
    def __init__(self, function, logger):
        self.logger = logger
        self.function = function

    def __enter__(self):
        self.start = datetime.datetime.now()

        return self

    def __exit__(self, *args):
        self.end = datetime.datetime.now()
        self.interval = self.end - self.start
        self.logger.info("%s took %0.2f seconds", self.function, self.interval.total_seconds())


def format_sql(sql, replace_sqlvar=None, replace_var=None, python=True):
    """Formats SQL query string for Python interpretation and with variables replaced.

    Args:
        sql (string): String with SQL query
        replace_sqlvar (dict, optional): If given, replaces variables of the format ${var:dict-key} with the value
            in the dictionary corresponding to that dict-key.
        replace_var (dict, optional): If given, replaces variables of the format {dict-key} with the value
            in the dictionary corresponding to that dict-key.
        python: If True, formats the query to be passed into a Python SQL querying function by replacing "%" with
            "%%" since % is a special character in Python

    Returns: string of SQL query with variables replaced and optionally formatted for Python

    """
    if replace_sqlvar is not None:
        for var in replace_sqlvar:
            sql = sql.replace("${var:%s}" % var, replace_sqlvar[var])

    if replace_var is not None:
        sql = sql.format(**replace_var)

    if python:
        sql = sql.replace("%", "%%")

    return sql


def read_csv_from_s3(bucket_name, bucket_folder, file_name):
    client = boto3.client('s3')
    obj = client.get_object(Bucket=bucket_name, Key=bucket_folder+file_name)
    df = pd.read_csv(obj['Body'])
    return df


def write_csv_to_s3(df, bucket_name, bucket_folder, file_name, arr=False):
    csv_buffer = StringIO()
    if(arr == False):
        df.to_csv(csv_buffer, index=False)
    else:
        np.savetxt(csv_buffer, df , delimiter=",")
    s3_resource = boto3.resource('s3')
    fq_feature_fname = bucket_folder+file_name
    s3_resource.Object(bucket_name, fq_feature_fname).put(Body=csv_buffer.getvalue())
