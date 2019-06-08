import traceback
from flask import render_template, request, redirect, url_for
import logging.config
import src.config as config
# from app.models import Tracks
from flask import Flask
from src.data_ingest_schema_create import UserInput
from flask_sqlalchemy import SQLAlchemy
import boto3

# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from flask_config.py
app.config.from_pyfile('src/config.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
#logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger("airbnbbookingprediction")
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)


@app.route('/')
def index():
    """Main view that lists songs in the database.

    Create view into index page that uses data queried from Track database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """

    try:
        tracks = db.session.query(UserInput).limit(app.config["MAX_ROWS_SHOW"]).all()
        logger.debug("Index page accessed")
        return render_template('index.html', tracks=tracks)
    except:
        traceback.print_exc()
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """View that process a POST with new song input

    :return: redirect to index page
    """

    try:
        user1 = UserInput(Age=request.form['age']
                         , Gender=request.form['gender']
                         , SignupMethod=request.form['signupmethod']
                         , Language=request.form['language']
                         , DateAccountCreated=request.form['dateaccountcreated'])
        db.session.add(user1)
        db.session.commit()
        logger.info("New user %s added aged %s", request.form['Gender'], request.form['Age'])
        return redirect(url_for('index'))
    except:
        logger.warning("Not able to display users, error page returned")
        return render_template('error.html')