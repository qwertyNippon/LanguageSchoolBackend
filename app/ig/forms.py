from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = StringField('Body of Post')
    img_url = StringField('Image URL')
    submit = SubmitField()

class UpdatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = StringField('Body of Post')
    img_url = StringField('Image URL')
    submit = SubmitField()

