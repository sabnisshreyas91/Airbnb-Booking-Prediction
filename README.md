# Airbnb Next Booking Prediction

<!-- toc -->
* Developer: [Shreyas Sabnis](https://github.com/sabnisshreyas91)
* QA: [Carson Chen](https://github.com/carsonzchen)
  
___

- [Project Charter](#project-charter)
- [Project Backlog](#project-backlog)
- [Running the application](#running-the-application)

    * [1) Set up the environment](#1-set-up-the-environment)
    * [2) Set up configurations](#2-set-up-configurations)
    * [3) Upload data and setup database schema](#3-upload-data-and-setup-database-schema)
    * [4) Train, Evaluate model & Run app](#4-train-evaluate-model-&-run-app)
    * [5) Testing](#5-testing)

<!-- tocstop -->

## Project Charter 

### Vision  
 To empower the business to predict travel trends of the user 
base to major destinations. This will allow execution of pro-active/remedial 
actions w.r.t marketing campaigns and host acquisition. This will also enable
 formulation of deals and discounts for specific customers to further drive 
 up bookings.  

### Mission
To predict which country a user will visit next, based on currently available data on 
demographics, web sessions and summary statistics on the users and countries
interest. Note that the mission does not include a prediction of when the customer
may make the next booking. This is because one of the business goals of 
the project is to leverage the prediction of *where* the user travel to next in 
order to influence *when* he me makes his next booking.

### Success criteria 

**Model Criterion**: The classification outcome labels consist of 10 individual countries, 'other' minor countries and 'NDF' which signifies no booking was made. Nearly 60% of rows have 'NDF' as the outcome label. Therefore the model is successful if the Cross Validation *Correct Classification Rate* significantly exceeds 40%. In addition prediction *precision* for each output label must exceed 70%.

**Desired Business Outcomes**: The first measure of project success would be the extent of traction and engagement it receives within the company, specifically by teams that are responsible for marketing/promotions and host acquisition. In the medium term, project success would be measured by an increase in booking-conversion rates, as users who are on the fence about a booking should be hit with relevant discounts/promotions that would encourage them to complete their booking. A long term indication of the models’ success would be a simultaneous increase in host acquisition, as well as user-bookings to countries with a high travel forecast.  
  

## Planning

### Theme
Forecast travel destinations of the user-base to inform strategic 
activities such as host acquisition, marketing campaigns and promotions.

### Epics

**1. Model Development**:
Gain familiarity with the data, explore relationships between various
user features and the likelihood of a user booking a stay at a specific country.
Formulate modelling approaches, test and select best subset of features and the
best performing model. 

*Stories*:-
* Data Cleansing - addressing missing / incoherent / incorrect data
* Exploratory Data Analysis
* Outlier detection and Management
* Feature Engineering
* Model selection and parameter tuning
* Model Evaluation
* Model performance and Reproducibility tests

### Backlog

1. *Model Development . Data Cleansing* (2)
2. *Model Development . Exploratory Data Analysis* (4)
3. *Model Development . Outlier detection and Management* (2)
4. *Model Development . Feature Engineering* (8)
5. *Model Development . Model selection and parameter tuning* (8)
6. *Model Development . Model Evaluation* (2)
7. *Model Development . Model performance test* (4)
8. *RDS . Schema and interaction scripts* (4)
8. *Flask . Form, front-end and interaction of app with database* (8)
9. *EC2 . Deployment, testing and persistence of app* (8)

### Icebox

* **User interface enhancement**:
Add captivating images and other cosmetic elements to front-end.


## Running the application

### 1. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. See bottom of README for exploratory data analysis environment setup. 

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv airbnbbookingprediction

source airbnbbookingprediction/bin/activate

pip install -r requirements.txt

```
#### With `conda`

```bash
conda create -n airbnbbookingprediction python=3.7
conda activate airbnbbookingprediction
pip install -r requirements.txt

```
### 2. Set up configurations
Currently, the app performs the following:

1) Extracts data from source and uploads to an S3 bucket of choice (as configured in src/config.py)
2) Creates database schema in either local sqlite server or AWS RDS server (again, both as configured in src/config.py)

#### i) To set up in local sqlite database 
Update src/config.py and set RDS_FLAG = 'F'
 
 OR

#### ii)To set up in AWS RDS
- Update src/config.py as set RDS_FLAG = 'T'
- Setup evironment variables
    - Update config/.mysqlconfig and update environment variables MYSQL_USER and MYSQL_PASSWORD as per the AWS RDS instance setup
    - Add the above environments to your bash profile by running:
    ```bash
    echo '~/Airbnb-Booking-Prediction/config/.mysqlconfig' >> ~/.bash_profile
    source ~/.bash_profile
    ```
Once step i) or ii) have been completed, verify the below configurations are setup in src/config.py :

- BUCKET_NAME -> The name of your destination AWS S3 bucket. 

(Note: The project requires *aws configure* to be run and the files ~/.aws/config and ~/.aws/credentials to exist so boto3 can identify them)

- BUCKET_FOLDER -> The name of the input folder within your S3 bucket where you wish to upload the data

- RDS_HOST -> The endpoint of your RDS instance

- RDS_PORT -> The port number associated with your RDS instance

### 3) Upload data and setup database schema
`python run.py --bucket_name=<bucket_name> --bucket_folder=<bucket_folder>`

(replace <bucket_name> and <bucket_folder> with the name of your AWS bucket and folder names. if no either one of them are not specified, the default values
as in the config.py file will be taken)

This command will, as described above:

1) Upload the source data to your target S3 bucket
2) Setup the database schema either in local sqlite or AWS RDS

### 4) Train, Evaluate model & Run app.
`make all`

This command will, as described above:

1) Read in the raw data to generate features and labels
2) Split up the features and labels into train/test
3) Train the model using the training data
4) Evaluate the model and save model details and evaluation metrics
5) Run the app

Alternatively, to perform each step individually:

1) Read in the raw data to generate features and labels
    
    `python src/generate_features_labels.py`
2) Split up the features and labels into train/test
   
    `python src/generate_train_test_split.py`
3) Train the model using the training data
   
    `python src/train_model.py`
4) Evaluate the model and save model details and evaluation metrics
   
    `python src/evaluate_model.py`
5) Run the app
   
    `python app.py`
	
### 5) Testing.
`pytest unit_test.py`

this will run the unit test for functions
