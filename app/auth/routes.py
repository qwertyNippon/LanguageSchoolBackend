from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import RegisterForm, LoginForm
from ..models import User
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash


auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/register', methods=['GET', 'POST'])
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
            user.save_user()

            flash('You\'re one of us now, well done!', 'success')
            return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            user_name = form.username.data
            password = form.password.data
            # print(user_name, password)

            user = User.query.filter_by(username=user_name).first()
            if user:
                print(user.password)
                if check_password_hash(user.password, password):
                # if user.password == password:  ---> Old way, NOT secure!
                    flash('sweet, you\'re logged in!', 'success')
                    login_user(user)
                    return redirect(url_for('ig.feed'))
                else:
                    flash('WRONG pass!', 'danger')
            else:
                flash('that user doesn\'t exist', 'warning')

            # user = db.session.execute(db.select(User).filter_by(username=user_name))   ---> newer syntax, I still prefer the old!
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    flash('you\'re logged out, have a great day!', 'secondary')
    logout_user()
    return redirect(url_for('land'))

