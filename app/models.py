from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

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
