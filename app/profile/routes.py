# profile/routes.py
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from .models import Profile, Student
from .forms import ProfileForm
from .. import db
import logging

bp = Blueprint('profile', __name__, template_folder='profile_templates')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

logging.basicConfig(level=logging.DEBUG)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/Profile', methods=['GET', 'POST'])
@login_required
def save_profile():
    logging.debug('Request method: %s', request.method)

    if request.method == 'GET':
        profile = Profile.query.filter_by(username=current_user.username).first()
        if profile:
            return jsonify({
                'username': profile.username,
                'firstname': profile.firstname,
                'lastname': profile.lastname,
                'email': profile.email,
                'bio': profile.bio,
                'language': profile.language,
                'level': profile.level,
                'certz': profile.certz,
                'photo': profile.photo
            }), 200
        else:
            return jsonify({'error': 'Profile not found'}), 404

    elif request.method == 'POST':
        form = ProfileForm()
        if form.validate_on_submit():
            logging.debug('Received form data: %s', form.data)
            bio = form.bio.data
            username = form.username.data
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            language = form.Language.data
            level = form.Level.data
            certz = form.Certz.data

            if form.photo.data and allowed_file(form.photo.data.filename):
                filename = secure_filename(form.photo.data.filename)
                photo_path = os.path.join(UPLOAD_FOLDER, filename)
                form.photo.data.save(photo_path)
            else:
                photo_path = None

            save_profile_to_database(username, firstname, lastname, email, bio, language, level, certz, photo_path)
            return jsonify({'message': 'Profile saved successfully'}), 200

        return jsonify({'error': 'Invalid form data'}), 400

def save_profile_to_database(username, firstname, lastname, email, bio, language, level, certz, photo_path):
    logging.debug('Saving profile to database')
    profile = Profile.query.filter_by(username=current_user.username).first()
    if profile:
        # Update existing profile
        profile.firstname = firstname
        profile.lastname = lastname
        profile.email = email
        profile.bio = bio
        profile.language = language
        profile.level = level
        profile.certz = certz
        if photo_path:
            profile.photo = photo_path
    else:
        # Create new profile
        profile = Profile(
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
        db.session.add(profile)
    
    db.session.commit()

@bp.route('/students/selected', methods=['GET'])
@login_required
def get_selected_students():
    selected_students = Student.query.filter_by(is_selected=True).all()
    students_list = [student.to_dict() for student in selected_students]
    return jsonify(students_list), 200
