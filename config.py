import os
import redis

basedir = os.path.abspath(os.path.dirname(__name__))

class Config():
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_NOTIFICATIONS=False
    STRIPE_KEY = os.environ.get('STRIPE_KEY')

    # SQLALCHEMY_ECHO = True
    # SESSION_TYPE = "redis"
    # SESSION_PERMANENT = False
    # SESSION_USE_SIGNER = True
    # SESSION_REDIS = redis.from_url("redis://127.0.0.1:5000")