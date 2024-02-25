# from flask import Blueprint, render_template, request, redirect, url_for, flash
# from flask_login import current_user, login_required

# from .forms import CreatePostForm, UpdatePostForm
# from ..models import Post, User

# myLessons = Blueprint('myLessons', __name__, template_folder='ig_templates' )

# @myLessons.route('/post/create', methods=['GET', 'POST'])
# @login_required
# def create_post():
#     form = CreatePostForm()
#     if request.method == 'POST':
#         if form.validate():
#             title = form.title.data
#             body = form.body.data
#             img_url = form.img_url.data

#             new = Post(title, body, img_url, current_user.id)
#             new.save_post()
#             return redirect(url_for('myLessons'))
#     return render_template('create_post.html', form=form)