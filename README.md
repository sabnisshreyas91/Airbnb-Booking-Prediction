# Airbnb Next Booking Prediction

<!-- toc -->
- [test](https://github.com/sabnisshreyas91/Airbnb-Booking-Prediction)
- [Project Charter](#project-charter)
- [Project Backlog](#project-backlog)

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

1. *Model Development . Data Cleansing* (2) - PLANNED
2. *Model Development . Exploratory Data Analysis* (4) - PLANNED
3. *Model Development . Outlier detection and Management* (2) - PLANNED
4. *Model Development . Feature Engineering* (8) - PLANNED
5. *Model Development . Model selection and parameter tuning* (8)
6. *Model Development . Model Evaluation* (2)
7. *Model Development . Model performance and Reproducibility tests* (4)

### Icebox

* **Set up S3 instance**:
This will be used to store the pickled model that will be used for making
predictions on user-input data.

* **Initialize RDS database**:
The RDS will be used to store cleansed training data in order to perform
the initial training of the best performing model. The trained model will be
pickled and stored in the S3 instance and used for all future predictions.

* **Deploy model using Flask**:
Write scripts to train the model using data stored in RDS, obtain user inputs
to feed as model data inputs and display model output.

* **User interface enhancement**:
Add captivating images and other cosmetic elements to front-end.
