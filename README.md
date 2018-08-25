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
## Run the server
- CMD: 
```
set FLASK_APP=app
python -m flask run
```
OR
- powerShell: 
```
$env:FLASK_APP = "app"
python -m flask run
```
## Run in browser
Forms List Page - http://localhost:5000/
Form Builder Page - http://localhost:5000/formBuilder
Form Submit Page - http://localhost:5000/submit/<id>
Form Submissions Page - http://localhost:5000/submission/<id>
