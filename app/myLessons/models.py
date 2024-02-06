from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


follows = db.Table(
    'follows',
    db.Column('followed_by_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('following_id',db.Integer, db.ForeignKey('user.id'), nullable=False)
)



class MyLessons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String)
    img_url = db.Column(db.String)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # liked = db.relationship('User',
    #         secondary = 'likes',
    #         backref = 'liked',
    #         lazy = 'dynamic'
    #             )

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

    def like_post(self, user):
        self.liked.append(user)
        db.session.commit()

    def unlike_post(self, user):
        self.liked.remove(user)
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