from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from .models import User
from .models import Post
from . import db

post = Blueprint('post', __name__)

@post.route('/post')
def posts():
    return "Posts"

@post.route('/post/<int:id>')
def post_view(id):
    post = Post.query.filter_by(id=id).first()
    post_author = User.query.filter_by(id=post.author_id).first()
    return render_template('post/post_view.html', post=post, user=post_author)

@post.route('/post/create', methods=['GET', 'POST'])
@login_required
def post_create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        post = Post.query.filter_by(title=title).first()

        if post:
            flash('Пост с таким же названием уже существует.')
            return redirect(url_for('post.post_create'))

        new_post = Post(author_id=current_user.id, title=title, content=content)

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('main.profile'))
    else:
        return render_template('post/post_create.html')