import traceback
from flask import render_template, request, redirect, url_for
import flask
import logging.config
import src.config as config
from src.helpers.helpers import read_csv_from_s3, read_array_from_s3
# from app.models import Tracks
from flask import Flask
import pickle
import boto3
import argparse
from io import BytesIO
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the Flask application
app = Flask(__name__,template_folder='app/templates/')
app.config.from_pyfile(os.path.join('config','flask_config.py'))

logger = logging.getLogger(__name__)
# Use pickle to load in the pre-trained model.

s3 = boto3.resource('s3')
parser = argparse.ArgumentParser()
parser.add_argument("--bucket_name", default= config.DEFAULT_BUCKET_NAME, help="S3 bucket to upload the source data to. Default:nw-shreyassabnis-msia423")
args = parser.parse_args()

df_train = read_csv_from_s3(args.bucket_name, config.DEFAULT_BUCKET_FOLDER, config.TRAIN_DATA)
genders = list(df_train.gender.unique())
signup_methods = list(df_train.signup_method.unique())
languages = list(df_train.language.unique())
affiliate_channels = list(df_train.affiliate_channel.unique())

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
        return(flask.render_template('index.html', genders = genders, signup_methods = signup_methods, languages = languages, affiliate_channels = affiliate_channels ))
    if flask.request.method == 'POST':

        gender_resp = flask.request.form['gender']
        signupmethod_resp = flask.request.form['signupmethod']
        language_resp = flask.request.form['language']
        affiliatechannel_resp = flask.request.form['affiliatechannel']
        

        gender = 'gender_'+gender_resp
        signupmethod = 'signup_method_'+signupmethod_resp
        language = 'language_'+language_resp
        affiliatechannel = 'affiliate_channel_' +affiliatechannel_resp

        feature_mode = read_csv_from_s3(args.bucket_name, config.FEATURE_FOLDER, config.MODE_FEATURES_FILE_NAME)
        training_data = read_csv_from_s3(args.bucket_name, config.FEATURE_FOLDER, config.TRAIN_FEATURE_FILE, nrows=1)
        labels = read_csv_from_s3(args.bucket_name, config.FEATURE_FOLDER, config.LABEL_FILE_NAME)
        le = LabelEncoder()
        y = le.fit_transform(labels)

        input_variables = pd.DataFrame([[gender, signupmethod, language, affiliatechannel]],columns=['gender', 'signupmethod', 'language', 'affiliatechannel'])

        upd_col_lst = [gender, signupmethod, language, affiliatechannel]
        for upd_col in upd_col_lst:
            try:
                feature_mode[upd_col]=1
            except:
                logger.warning("column %s does not exist in training data, ignoring update", upd_col)
        
        prediction = model.predict_proba(feature_mode[list(training_data)].values)
        y_pred_names = []
        for i in range(len(prediction)):
            y_pred_names.append(list(le.inverse_transform(np.argsort(prediction[i])[::-1])[:2]))
        pred_val = y_pred_names[0][0]+","+y_pred_names[0][1]

        return flask.render_template('index.html',
                                        original_input={'Gender':gender_resp,
                                                        'signupmethod':signupmethod_resp,
                                                        'language':language_resp,
                                                        'affiliatechannel':affiliatechannel_resp
                                                        },
                                        result=pred_val, genders = genders, signup_methods = signup_methods, languages = languages, affiliate_channels = affiliate_channels 
                                        )

if __name__ == '__main__':
    app.run(host = app.config['HOST'],port=app.config['PORT'],debug=app.config['DEBUG'])
