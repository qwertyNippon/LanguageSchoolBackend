from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    firstname = db.Column(db.String(50), nullable=False, unique=False)
    lastname = db.Column(db.String(50), nullable=False, unique=False)
    email = db.Column(db.String(120), nullable=False, unique=True)  # Added length to email field
    bio = db.Column(db.String(300), nullable=True, unique=False)
    certz = db.Column(db.String(300), nullable=True, unique=False)
    language = db.Column(db.String(100), nullable=True, unique=False)
    level = db.Column(db.String(100), nullable=True, unique=False)
    photo = db.Column(db.String(255), nullable=True, unique=False)
    teacher = db.relationship('Teacher', uselist=False, back_populates='profile')
    student = db.relationship('Student', uselist=False, back_populates='profile')

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    profile = db.relationship('Profile', back_populates='student')
    lesson_balance = db.Column(db.Integer)
    is_selected = db.Column(db.Boolean, default=False)

    def __init__(self, profile_id, lesson_balance=0):
        self.profile_id = profile_id
        self.lesson_balance = lesson_balance

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'profile_id': self.profile_id,
            'lesson_balance': self.lesson_balance,
            'is_selected': self.is_selected,
            'name': self.profile.firstname if self.profile else None,  # Assuming you want to include the profile's firstname
            'avatarUrl': self.profile.photo if self.profile else None  # Assuming you want to include the profile's photo
        }
