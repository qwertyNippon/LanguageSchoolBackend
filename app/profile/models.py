from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    firstname = db.Column(db.String(50), nullable=False, unique=False)
    lastname = db.Column(db.String(50), nullable=False, unique=False)
    email = db.Column(db.String, nullable=False, unique=True)
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

    def to_dict(self):
        return {
            'name': self.profile.firstname,  # Use firstname from Profile
            'avatarUrl': self.profile.photo,  # Use photo from Profile
            'lessonBalance': self.lesson_balance,
            'isSelected': self.is_selected,
        }