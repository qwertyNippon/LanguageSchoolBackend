from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import RegisterForm, LoginForm
from ...models import User
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy

auth = Blueprint('auth', __name__, template_folder='auth_templates')

db = SQLAlchemy()
def save_me(self):
    db.session.add(self)
    db.session.commit()

@auth.route('/signup', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print(request.method)
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            print(username, email, password)

            user = User(username, email, password)
            user.save_me()

            data = request.get_json()
            return redirect(url_for('login_user'))
            # expectation is for the page to change 
            # to the login page oce data is inputted 
            # for the line above.
    print(data)

    return 'ok'

# *********TESTING below code

@auth.route('/login', methods=["POST"])
def login_user():
    data = request.json
    print(data)
    u = data['username']
    user = User.query.filter_by(username=u).first()
    if user:
        if check_password_hash(user.password, data['pass']):
            return {
                'status':'ok',
                'message' : 'Logged in!',
                'data':{
                    'user': user.to_dict(),
                    'token': ''
                }  
            }
        else:
            return {
                'status' : 'NOT ok',
                'message': 'Wrong Password',
                }, 400
    return {
        'status': 'NOT ok',
        'message': "username no existe",
        'error': 'no username match'
    }, 418


@auth.route('/logout')
def logout():
    flash('you\'re logged out, have a great day!')
    logout_user()
    return redirect(url_for('Home'))