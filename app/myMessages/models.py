from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class MyMessages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __init__(self, body):
        # self.title = title
        self.body = body
        # self.img_url = img_url
        # self.user_id = user_id

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
            # 'title': self.title,
            'body': self.body,
            # 'img' : self.img_url,
            'date_created': self.date_created,
            # 'user_id': self.user_id,
            # 'author' : self.author.username
        }