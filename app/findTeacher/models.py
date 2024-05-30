from flask_sqlalchemy import SQLAlchemy
from ..profile.models import db

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    profile = db.relationship('Profile', back_populates='teacher')
    language = db.Column(db.String(100)) 
    firstname = db.Column(db.String(50))
    bio = db.Column(db.String(300))
    photo = db.Column(db.String(255))  # Path or filename of the uploaded photo

    def __repr__(self):
        return f"Teacher('{self.profile.username}', '{self.profile.email}', '{self.language}', '{self.firstname}', '{self.bio}')"
    