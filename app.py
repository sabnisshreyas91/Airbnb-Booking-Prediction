import traceback
from flask import render_template, request, redirect, url_for
import logging.config
import src.config as config
# from app.models import Tracks
from flask import Flask
import pickle
import boto3
import argparse
from io import BytesIO
import pandas as pd

# Initialize the Flask application
app = Flask(__name__,template_folder='app/templates/')

logger = logging.getLogger(__name__)

import flask
# Use pickle to load in the pre-trained model.

s3 = boto3.resource('s3')
parser = argparse.ArgumentParser()
parser.add_argument("--bucket_name", default= config.DEFAULT_BUCKET_NAME, help="S3 bucket to upload the source data to. Default:nw-shreyassabnis-msia423")
args = parser.parse_args()

with BytesIO() as data:
    s3.Bucket(args.bucket_name).download_fileobj(config.MODEL_S3_LOCATION, data)
    data.seek(0)    # move back to the beginning after writing
    model = pickle.load(data)

@app.route('/', methods=['GET','POST'])
def index():
    """Main view that lists songs in the database.

    Create view into index page that uses data queried from Track database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
    if flask.request.method == 'POST':
        gender = flask.request.form['gender']
        signupmethod = flask.request.form['signupmethod']
        language = flask.request.form['language']
        affiliatechannel = flask.request.form['affiliatechannel']
        input_variables = pd.DataFrame([[gender,age,signupmethod,language,affiliatechannel]],
                                       columns=['gender','age','signupmethod','language','affiliatechannel'],
                                       dtype=float)
        print(input_variables)


if __name__ == '__main__':
    app.run()