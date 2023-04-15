from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import desc

from .models import User
from .models import Post
from .models import Comment
from . import db

post = Blueprint('post', __name__)

@post.route('/post')
def index():
    posts = []
    q_posts = Post.query.order_by(desc(Post.id)).all()
    
    for post in q_posts:
        post_author = User.query.filter_by(id=post.author_id).first()
        if post and post_author.ban != 1:
            posts.append(post)

    return render_template('post/list.html', posts=posts)

@post.route('/post/<int:id>', methods=['GET', 'POST'])
def view(id):
    if request.method == "POST":
        if current_user.ban != 1:
            author_id = current_user.id
            content = request.form.get('content')
            
            if content.replace(" ", "") != "":
                new_user = Comment(post_id=id, author_id=author_id, content=content)

                db.session.add(new_user)
                db.session.commit()

        return redirect(url_for("post.view", id=id))
    else:
        post = Post.query.filter_by(id=id).first()
        if post:
            post_author = User.query.filter_by(id=post.author_id).first()

            if post_author.ban == 1:
                return redirect(url_for("main.profile") + "/" + str(post_author.id))
            else:
                post_comments = Comment.query.filter_by(post_id=post.id)
                comments = []
                for comment in post_comments:
                    comment_author = User.query.filter_by(id=comment.author_id).first()
                    if comment and comment_author.ban != 1:
                        comments.append([comment_author.name, comment_author.admin, comment.content, comment_author.id])

                return render_template('post/view.html', post=post, user=post_author, comments=reversed(comments))
        else:
            return render_template('error/not_found.html', message="Пост не найден.")

@post.route('/post/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        if current_user.ban != 1:
            title = request.form.get('title')
            content = request.form.get('content')

            post = Post.query.filter_by(title=title).first()

            if post:
                flash('Пост с таким же названием уже существует.')
                return redirect(url_for('post.create'))

            new_post = Post(author_id=current_user.id, title=title, content=content)

            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for('main.profile'))
        else:
            flash('Ваш аккаунт заблокирован, вы не можете создавать публикации.')
            return redirect(url_for('post.create'))
    else:
        return render_template('post/create.html')