from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CreatePostForm(FlaskForm):
    body = StringField('Body of text', validators=[DataRequired()])
    submit = SubmitField()

class UpdatePostForm(FlaskForm):
    body = StringField('Body of text', validators=[DataRequired()])
    submit = SubmitField()