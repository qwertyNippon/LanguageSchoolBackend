# auth/routes.py
from flask import Blueprint, request, redirect, url_for, flash, jsonify
from .forms import RegisterForm, LoginForm
from ..models import User
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user = User(username, email, password)
    user.save_user()

    return jsonify({"message": "Registration successful"}), 200

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_name = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=user_name).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@auth.route('/logout')
def logout():
    logout_user()
    return redirect('http://localhost:5173/')
