from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=50)])
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=1, max=50)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    bio = TextAreaField('Bio', validators=[Length(max=300)])
    Certz = TextAreaField('Certificates', validators=[Length(max=300)])
    Language = StringField('Language', validators=[Length(max=100)])
    Level = StringField('Level', validators=[Length(max=100)])
    photo = FileField('Upload Photo') 
    submit = SubmitField('Save')