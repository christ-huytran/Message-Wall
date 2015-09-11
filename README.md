# Message Wall

A message dashboard that runs on the Flask microframework for Python

## To Run Locally
Note #1: The creator of Flask recommends setting up virtualenv to avoid running into Python libraries version compatibility issues. Skip this step if you already have virtualenv and Flask installed on your system.

Note#2: I have included the ERD (Entity Relationship Diagram) file for the MySQL database schema as well as a .sql script to generate the required tables. Please generate a schema and start your database server before doing the following steps.
```
# Install Virtual Environment
sudo pip install virtualenv
```
Navigate into your project folder and set up venv folder:
```
# Set up venv
virtualenv venv
```
```
# Activate venv
. venv/bin/activate
```
Then you can get all of the required packages activated in your virtualenv:
```
# Install required packages with pip
pip install -r requirements.txt
```
And finally:
```
# Start the server
python server.py
```
If you run into any problem, you could consult Flask documentation [here](http://flask.pocoo.org/docs/0.10/installation/#installation).

Enjoy!

