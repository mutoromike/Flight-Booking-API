[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4dc0116c2a1349b6893a48334030dc51)](https://app.codacy.com/app/mutoromike/Flight-Booking-API?utm_source=github.com&utm_medium=referral&utm_content=mutoromike/Flight-Booking-API&utm_campaign=Badge_Grade_Dashboard)  [![Coverage Status](https://coveralls.io/repos/github/mutoromike/Flight-Booking-API/badge.svg?branch=develop)](https://coveralls.io/github/mutoromike/Flight-Booking-API?branch=develop)  [![CircleCI](https://circleci.com/gh/mutoromike/Flight-Booking-API/tree/master.svg?style=svg)](https://circleci.com/gh/mutoromike/Flight-Booking-API/tree/master)

## Documentation 
-   The documentation link is https://flightapiflask.docs.apiary.io/

# Flight-Booking-API

This is an API that powers a FLIGHT BOOKING APPLICATION. It allows clients to book tickets and track their flight details. The system also reminds the clients about their flights with a 24 hour notice. 

## The applicaton enables the user to

-   Sign-Up
-   Log in
-   Upload passport photographs (changing and deleting also supported)
-   View available flights
-   Book tickets/reservations
-   Receive tickets as an email
-   Check the status of their flight
-   Remind clients about their flights (24 hr notice)

## Tech/Framework used

The application has been built by:

Flask (Python)

## Installation

### Ensure you have
    - `python 3+ installed`
    - installed `virtual environment`
    - Clone the repo to your local machine
    - Navigate to bright_events folder
    - Create a virtual environment and run the command: `pip install -r requirements.txt` (install packages)

### Start the application
    - Run the following to start the app:
`python run.py`
    - Navigate to postman to test the api endpoints

### Tests
 To run tests and ensure the application works:

    - Navigate to tests folder on cmd or terminal
    - Run the command `python manage.py test`

### Using the application
    - Register to create an account
    - Login using username and password created
    - After signing in you can proceed to book a upload a passport photo, then you can book and track flights
