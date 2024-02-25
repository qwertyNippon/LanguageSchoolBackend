from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from .forms import CreatePostForm, UpdatePostForm
from ..models import Post, User

myMessages = Blueprint('myMessages', __name__, template_folder='ig_templates' )

@myMessages.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if request.method == 'POST':
        if form.validate():
            body = form.body.data

            new = Post(body, current_user.id)
            new.save_post()
            return redirect(url_for('myMessages'))
    return render_template('create_post.html', form=form)