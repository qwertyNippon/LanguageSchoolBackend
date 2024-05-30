from flask_sqlalchemy import SQLAlchemy
from ..profile.models import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    profile = db.relationship('Profile', back_populates='student')
    language = db.Column(db.String(100)) 
    firstname = db.Column(db.String(50))
    bio = db.Column(db.String(300))
    lesson_balance = db.Column(db.Integer)
    is_selected = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Student('{self.profile.username}',
          '{self.profile.email}', 
          '{self.language}', 
          '{self.firstname}', 
          '{self.bio}',
          '{self.lesson_balance}',
          '{self.is_selected}',
          )"
    