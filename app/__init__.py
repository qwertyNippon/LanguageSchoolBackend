# app/__init__.py
from flask import Flask, redirect
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_cors import CORS
from flask_socketio import SocketIO
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

# Blueprints
from .auth.routes import auth
from .myLessons.routes import myLessons
# from .myMessages.routes import myMessages
# from .api.routes import api
# from .payments.routes import payments

app.register_blueprint(auth)
app.register_blueprint(myLessons, url_prefix='/myLessons')
# app.register_blueprint(myMessages)
# app.register_blueprint(api)
# app.register_blueprint(payments)

# SocketIO routes
@app.route('/Classroom')
def index():
    # Redirect to a unique room ID
    return redirect('/Classroom/' + str(uuid.uuid4()))

# User loader callback for Flask-Login

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Import routes and models at the end to avoid circular imports
from . import routes
from .models import User, MyLessons

if __name__ == '__main__':
    socketio.run(app, debug=True)
