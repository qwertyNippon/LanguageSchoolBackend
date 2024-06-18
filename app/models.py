from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from app import db

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

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def follow(self, user):
        self.following.append(user)
        db.session.commit()

    def unfollow(self, user):
        self.following.remove(user)
        db.session.commit()

class MyLessons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String)
    img_url = db.Column(db.String)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, body, img_url, user_id):
        self.title = title
        self.body = body
        self.img_url = img_url
        self.user_id = user_id

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    def save_changes(self):
        db.session.commit()

    def delete_post(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'title': self.title,
            'body': self.body,
            'img' : self.img_url,
            'date_created': self.date_created,
            'user_id': self.user_id,
            'author' : self.author.username
        }

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    profile = db.relationship('Profile', back_populates='teacher')
    is_selected = db.Column(db.Boolean, default=False)

    def __init__(self, profile_id, is_selected):
        self.profile_id = profile_id
        self.is_selected = is_selected

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
            'specialty': self.specialty,
            'name': self.profile.firstname if self.profile else None,  # Assuming you want to include the profile's firstname
            'avatarUrl': self.profile.photo if self.profile else None  # Assuming you want to include the profile's photo
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
            'name': self.profile.firstname if self.profile else None,  # Assuming you want to include the profile's firstname
            'avatarUrl': self.profile.photo if self.profile else None  # Assuming you want to include the profile's photo
        }
    
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
