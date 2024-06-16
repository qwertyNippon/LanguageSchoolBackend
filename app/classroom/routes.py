from flask import render_template, redirect, url_for, request
from . import app, db
from .models import User
from flask_login import login_required, current_user
from .forms import RegistrationForm
from flask import Flask, request, jsonify

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    # Process the received data
    return jsonify({'message': 'Data received successfully'})