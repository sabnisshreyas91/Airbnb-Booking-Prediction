# Airbnb Next Booking Prediction

<!-- toc -->

- [Project Charter](#project-charter)
- [Project Backlog](#project-backlog)

<!-- tocstop -->

## Project Charter 

### Vision  
To predict which country a user will visit next, based on 
demographics, web sessions and summary statistics.

### Mission
 To empower the business to predict travel trends of the user 
base to major destinations. This will allow execution of pro-active/remedial 
actions w.r.t marketing campaigns and host acquisition. This will also enable
 formulation of deals and discounts for specific customers to further drive 
 up bookings.  

### Success criteria 

**Model Criterion**: The classification outcome labels consist of 10 individual countries, 'other' minor countries and 'NDF' which signifies no booking was made. Nearly 60% of rows have 'NDF' as the outcome label. Therefore the model is successful if the *Correct Classification Rate* exceeds 40%.

**Desired Business Outcomes**: If the model is successful, 
 then *booking-conversion* rates should increase, as users who are on the 
 fence about a holiday will be hit with relevant deals and discounts 
 encouraging them to complete their bookings. 
 A long term indication of the models' success would be a simultaneous 
 increase in *Host Acquisition* as well as user trips to countries \
 with a high travel forecast.   
  

## Project Backlog 

### Theme
Forecast travel destinations of the user-base to inform strategic 
activities such as host acquisition, marketing campaigns and promotions.

### Epics

**Model Development**:
Gain familiarity with the data, explore relationships between various
user features and the likelihood of a user booking a stay at a specific country.
Formulate modelling approaches, test and select best subset of features and the
best performing model. 

*Stories*:
* Data Cleansing
* Exploratory Data Analysis
* Outlier detection and Management
* Feature Engineering
* Model selection and parameter tuning
* Model Evaluation
* Model performance and Reproducibility tests

