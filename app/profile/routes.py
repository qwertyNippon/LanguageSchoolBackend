# Import necessary modules
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

# Importing the SQLAlchemy instance
from . import db

# Importing the Profile model
from ..models import Profile

# Create a Blueprint for the routes
bp = Blueprint('routes', __name__)

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# POST endpoint to save profile data including photo
@bp.route('/Profile', methods=['POST'])
def save_profile():
    # Get form data
    data = request.form
    bio = data.get('bio')
    username = data.get('username')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    language = data.get('language')
    level = data.get('level')
    
    # Get the file from the request
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

    # Save the profile data to the database
    save_profile_to_database(username, firstname, lastname, email, bio, language, level, photo_path)

    return jsonify({'message': 'Profile saved successfully'}), 200

# Function to save profile data to database
def save_profile_to_database(username, firstname, lastname, email, bio, language, level, photo_path):
    # Create a new Profile object with the provided data
    new_profile = Profile(
        username=username,
        firstname=firstname,
        lastname=lastname,
        email=email,
        bio=bio,
        language=language,
        level=level,
        photo=photo_path
    )

    # Add the new profile to the database session
    db.session.add(new_profile)

    # Commit the changes to the database
    db.session.commit()


# Function to delete bio from database
def delete_bio_from_database(bio_id):
    # Query the database for the profile with the provided bio_id
    profile = Profile.query.get(bio_id)

    # If profile with the provided bio_id exists, delete it from the database
    if profile:
        db.session.delete(profile)
        db.session.commit()
        return jsonify({'message': 'Bio deleted successfully'}), 200
    else:
        return jsonify({'error': 'Profile not found'}), 404

# POST endpoint to delete a profile
@bp.route('/Profile/delete/<int:id>', methods=['POST'])
def delete_profile(id):
    # Query the database for the profile with the provided id
    profile = Profile.query.get(id)

    # If the profile exists, delete it from the database
    if profile:
        # Delete the associated photo file if it exists
        if profile.photo:
            photo_path = os.path.join(UPLOAD_FOLDER, profile.photo)
            if os.path.exists(photo_path):
                os.remove(photo_path)
        
        # Delete the profile from the database
        db.session.delete(profile)
        db.session.commit()
        return jsonify({'message': 'Profile deleted successfully'}), 200
    else:
        return jsonify({'error': 'Profile not found'}), 404