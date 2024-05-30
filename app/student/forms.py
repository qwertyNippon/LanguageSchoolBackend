from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class StudentForm(FlaskForm):
    language = StringField('Language', validators=[DataRequired(), Length(max=100)])
    firstname = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    bio = TextAreaField('Bio', validators=[Length(max=300)])
    submit = SubmitField('Submit')