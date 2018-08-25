from flask_sqlalchemy import SQLAlchemy


from app import app
db = SQLAlchemy(app)


class Form(db.Model):
    __tablename__ = "forms"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(50))
    submissions = db.Column(db.Integer)
    fields = db.relationship('Field', backref='form', lazy=True)


class Field(db.Model):
   __tablename__ = "fields"
   id = db.Column(db.Integer, primary_key=True)
   label = db.Column(db.String(50))
   name = db.Column(db.String(50))
   type = db.Column(db.String(50))
   form_id = db.Column(db.Integer, db.ForeignKey('forms.id'), nullable=False)
   submissions = db.relationship('Submission', backref='field', lazy=True)


class Submission(db.Model):
    __tablename__ = "submissions"
    user_id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id'), nullable=False,primary_key=True)
    input = db.Column(db.String(50))
