from flask import Flask
from config import Config
from .auth.routes import auth
# from .myLessons.routes import myLessons
# from .myMessages.routes import myMessages
from .models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
# from .api.routes import api
# from .payments.routes import payments
from flask_cors import CORS

from flask import Flask, render_template, redirect
from flask_socketio import SocketIO, join_room, leave_room
import uuid

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# ****************

@app.route('/Classroom')
def index():
    # Redirect to a unique room ID
    return redirect('/Classroom/' + str(uuid.uuid4()))

# @app.route('/some_other_route')
# def some_other_route():
    # Implement the logic for this route
    # return "This is some other route"

if __name__ == '__main__':
    socketio.run(app)

# ****************

app.config.from_object(Config)

login = LoginManager()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


db.init_app(app)
migrate = Migrate(app, db)

login.init_app(app)

login.login_view = 'auth.login'

moment = Moment(app)

app.register_blueprint(auth)
# app.register_blueprint(myLessons)
# app.register_blueprint(myMessages)
# app.register_blueprint(ig)
# app.register_blueprint(api)
# app.register_blueprint(payments)

from . import routes
from . import models