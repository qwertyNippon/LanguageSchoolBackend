# profile/routes.py
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
# from .. import db
from .models import Profile, Student
import logging

bp = Blueprint('routes', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

logging.basicConfig(level=logging.DEBUG)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/profile', methods=['POST'])
@login_required
def save_profile():
    logging.debug('Received request: %s', request.form)
    bio = request.form.get('bio')
    username = request.form.get('username')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    language = request.form.get('language')
    level = request.form.get('level')
    certz = request.form.get('certz')

    if 'photo' in request.files:
        photo = request.files['photo']
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(UPLOAD_FOLDER, filename)
            photo.save(photo_path)
        else:
            return jsonify({'error': 'Invalid file or file format not allowed'}), 400
    else:
        photo_path = None

    save_profile_to_database(username, firstname, lastname, email, bio, language, level, certz, photo_path)

    return jsonify({'message': 'Profile saved successfully'}), 200

def save_profile_to_database(username, firstname, lastname, email, bio, language, level, certz, photo_path):
    from .. import db
    logging.debug('Saving profile to database')
    new_profile = Profile(
        username=username,
        firstname=firstname,
        lastname=lastname,
        email=email,
        bio=bio,
        language=language,
        level=level,
        certz=certz,
        photo=photo_path
    )
    db.session.add(new_profile)
    db.session.commit()

@bp.route('/students/selected', methods=['GET'])
@login_required
def get_selected_students():
    # Query to get selected students
    selected_students = Student.query.filter_by(is_selected=True).all()
    students_list = [student.to_dict() for student in selected_students]
    return jsonify(students_list), 200
