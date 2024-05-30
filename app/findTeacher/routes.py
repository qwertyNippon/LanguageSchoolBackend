from flask import Blueprint, jsonify, request
from .models import db, Teacher

# Create a Blueprint for the routes
teacher_search_bp = Blueprint('teacher_search', __name__)

# Route for searching teachers
@teacher_search_bp.route('/FindTeacher', methods=['GET'])
def search_teacher():
    # Get query parameters from the request
    language = request.args.get('language')
    firstname = request.args.get('firstname')

    # Query the database based on the provided parameters
    teachers_query = Teacher.query

    # Prioritize searching by language
    if language:
        teachers_query = teachers_query.filter(Teacher.language.ilike(f'%{language}%'))

        # If language is found, return the teachers matching the language
        teachers = teachers_query.all()

        # Convert the results to JSON and return
        teachers_data = [{
            'id': teacher.id,
            'language': teacher.language,
            'firstname': teacher.firstname,
            'bio': teacher.bio
        } for teacher in teachers]

        return jsonify(teachers_data)

    # If language is not specified or no teachers are found matching the language,
    # continue searching by firstname
    if firstname:
        teachers_query = teachers_query.filter(Teacher.firstname.ilike(f'%{firstname}%'))

    # Execute the query and retrieve the results
    teachers = teachers_query.all()

    # Convert the results to JSON and return
    teachers_data = [{
        'id': teacher.id,
        'language': teacher.language,
        'firstname': teacher.firstname,
        'bio': teacher.bio
    } for teacher in teachers]

    return jsonify(teachers_data)
