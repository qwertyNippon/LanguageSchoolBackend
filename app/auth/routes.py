# auth/routes.py
from flask import Blueprint, request, redirect, url_for, flash, jsonify
from .forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from app import db
from ..models import User
# Import db from app module

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/register', methods=['POST'])
def register():
    # from ..models import User  
    # Import User locally
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user = User(username, email, password)
    user.save_user()

    return jsonify({"message": "Registration successful"}), 200

@auth.route('/login', methods=['POST'])
def login():
    # from ..models import User 
    # Import User locally
    data = request.get_json()
    user_name = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=user_name).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"message": "authenticated", "data": {"username": user.username, "email": user.email}}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@auth.route('/protected')
@login_required
def protected_route():
    user = current_user
    return f"Protected Route: Hello, {user.username}!"

@auth.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200