# Background:
I've used the flask web framework in python.
# INSTALL (windows):
- pip install flask
- Anaconda3 library
- pip install flask-sqlalchemy
- pip install flask-socketio
- pip install Flask-Migrate

# How to migrate the models: 
- set FLASK_APP=app.py
- flask db init
- flask db migrate
- flask db upgrade
 
# RUN with cmd:
- cd FormBuilder
- CMD: 
> set FLASK_APP=app
OR
- powerShell: 
> $env:FLASK_APP = "app"
> python -m flask run
