# Profile/models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

follows = db.Table(
    'follows',
    db.Column('followed_by_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('following_id', db.Integer, db.ForeignKey('user.id'), nullable=False)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.Boolean, default=False)
    student = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    language = db.Column(db.String(100))
    myLessons = db.relationship('MyLessons', backref='author', lazy=True)
    following = db.relationship('User',
                                primaryjoin=(follows.c.followed_by_id == id),
                                secondaryjoin=(follows.c.following_id == id),
                                secondary=follows,
                                backref=db.backref('follows', lazy='dynamic'),
                                lazy='dynamic'
                                )
    profile = db.relationship('Profile', uselist=False, back_populates='user')


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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='profile')

    def __init__(self, username, firstname, lastname, email, bio=None, certz=None, language=None, level=None, photo=None, user_id=None):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.bio = bio
        self.certz = certz
        self.language = language
        self.level = level
        self.photo = photo
        self.user_id = user_id

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
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'bio': self.bio,
            'certz': self.certz,
            'language': self.language,
            'level': self.level,
            'photo': self.photo,
            'user_id': self.user_id
        }

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
            'firstname': self.profile.firstname if self.profile else None,  # Accessing the profile's firstname
            'avatarUrl': self.profile.photo if self.profile else None  # Accessing the profile's photo
        }
