from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from .forms import CreatePostForm, UpdatePostForm
from ..models import Post, User

ig = Blueprint('ig', __name__, template_folder='ig_templates' )


@ig.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if request.method == 'POST':
        if form.validate():
            title = form.title.data
            body = form.body.data
            img_url = form.img_url.data

            new = Post(title, body, img_url, current_user.id)
            new.save_post()
            return redirect(url_for('ig.feed'))
    return render_template('create_post.html', form=form)

@ig.route('/feed', methods=['GET'])
@login_required
def feed():
    # posts = Post.query.all()
    # posts = Post.query.order_by(Post.date_created.desc()).all()
    posts = Post.query.order_by(Post.date_created).all()[::-1]
    for p in posts:
        likes = p.liked.count()
        p.likes = likes

    # print(posts)

    return render_template('feed.html', posts=posts)

@ig.route('/post/<int:post_id>')
@login_required
def ind_post(post_id):
    post = Post.query.get(post_id)
    likes = post.liked.count()
    post.likes = likes
    my_likes = current_user.liked
    print(current_user.liked)
    for m in my_likes:
        if post.id == m.id:
            post.like_flag = True

    if post:
        return render_template('post.html', p = post)
    else:
        print('That post doesn\'t exist!')
    return redirect(url_for('ig.feed'))


@ig.route('/post/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get(post_id)
    if post.user_id != current_user.id:
        flash('This is not your post to modify!', 'danger')
        return redirect(url_for('ig.feed'))
    form = UpdatePostForm()
    if request.method == 'POST':
        if form.validate():
            title = form.title.data
            body = form.body.data
            img_url = form.img_url.data
            print(title, body, img_url)

            post.title = title
            post.body = body
            post.img_url = img_url
            post.save_changes()
            flash('post updated', 'secondary')
            return redirect(url_for('ig.ind_post', post_id=post.id))

    return render_template('update_post.html', form=form, post=post)


@ig.route('/post/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post.user_id == current_user.id:
        post.delete_post()
        flash('post is gone forever!', 'warning')
    else:
        flash("Can't delete what's not yours!", 'danger')
    return redirect(url_for('ig.feed'))

@ig.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    u = User.query.get(user_id)
    if u:
        current_user.follow(u)
        flash(f"You're now following {u.username}", 'success')
    else:
        flash('User does not exist!', 'danger')
    return redirect(url_for('land'))

@ig.route('/unfollow/<int:user_id>')
@login_required
def unfollow(user_id):
    u = User.query.get(user_id)
    if u:
        current_user.unfollow(u)
        flash(f"You're no longer following {u.username}", 'warning')
    else:
        flash('User does not exist!', 'danger')
    return redirect(url_for('land'))

@ig.route('/post/like/<int:post_id>')
@login_required
def like(post_id):
    post = Post.query.get(post_id)
    my_likes = current_user.liked
    print(my_likes)
    if post in my_likes:
        flash(f"You've already liked this one, you can't like it any more!", 'warning')
    else:
        post.like_post(current_user)
        flash("you've added a like to this post!", 'success')
    return redirect(url_for('ig.feed'))


@ig.route('/post/unlike/<int:post_id>')
@login_required
def unlike(post_id):
    post = Post.query.get(post_id)
    my_likes = current_user.liked
    if post in my_likes:
        post.unlike_post(current_user)
        flash(f"We don't like this one anymore", 'warning')
    else:
        flash("You didn't like this one anyways . . . ", 'danger')
    return redirect(url_for('ig.feed'))

