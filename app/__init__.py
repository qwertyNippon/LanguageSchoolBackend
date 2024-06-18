# app/__init__.py
from flask import Flask, redirect
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_session import Session
# from .auth.routes import auth
import uuid

# Initialize the Flask application
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'
moment = Moment(app)
Session(app)

# Blueprints
from .auth.routes import auth
from .myLessons.routes import myLessons
from .profile.routes import bp as profile_bp
# from .myMessages.routes import myMessages
# from .api.routes import api
# from .payments.routes import payments

app.register_blueprint(auth)
app.register_blueprint(myLessons, url_prefix='/myLessons')
app.register_blueprint(profile_bp, url_prefix='/profile')  # Register the profile blueprint

# app.register_blueprint(myMessages)
# app.register_blueprint(api)
# app.register_blueprint(payments)

# User loader callback for Flask-Login

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# SocketIO routes
@app.route('/Classroom')
def index():
    # Redirect to a unique room ID
    return redirect('/Classroom/' + str(uuid.uuid4()))

@app.route('/test_redis')
def test_redis():
    try:
        redis_client = app.config['SESSION_REDIS']
        redis_client.set('foo', 'bar')
        value = redis_client.get('foo')
        return f'Redis is working: {value}'
    except Exception as e:
        return f'Redis connection failed: {e}'

# Import routes and models at the end to avoid circular imports
from . import routes
from .models import User, MyLessons

if __name__ == '__main__':
    socketio.run(app, debug=True)
