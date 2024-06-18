from flask import Flask, jsonify, request
from config import Config
from models import db, Student, Profile
from ..profile.models import Profile
from flask_login import login_required, current_user

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(Config)
db.init_app(app)

@app.route('/students', methods=['GET'])
@login_required
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

@app.route('/students', methods=['POST'])
@login_required
def add_student():
    data = request.get_json()
    profile = Profile.query.filter_by(id=data['profile_id']).first()
    if profile:
        new_student = Student(
            profile_id=profile.id,
            lesson_balance=data.get('lessonBalance', 0),
            is_selected=data.get('isSelected', False)
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify(new_student.to_dict()), 201
    return jsonify({'error': 'Profile not found'}), 404

@app.route('/students/<int:student_id>/select', methods=['POST'])
@login_required
def select_student(student_id):
    student = Student.query.get(student_id)
    if student:
        # Unselect all students first
        Student.query.update({'is_selected': False})
        # Select the clicked student
        student.is_selected = True
        db.session.commit()
        return jsonify(student.to_dict()), 200
    return jsonify({'error': 'Student not found'}), 404

@app.route('/students/selected', methods=['GET'])
@login_required
def get_selected_student():
    student = Student.query.filter_by(is_selected=True).first()
    if student:
        return jsonify(student.to_dict()), 200
    return jsonify({'error': 'No student selected'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
