from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import desc

import datetime

from .models import User
from .models import Post
from .models import Comment
from . import db

post = Blueprint('post', __name__)

@post.route('/post')
def index():
    posts = []
    q_posts = Post.query.order_by(desc(Post.active)).order_by(desc(Post.id)).all()
    users = {}
    
    for post in q_posts:
        post_author = User.query.filter_by(id=post.author_id).first()
        if post and post_author and post_author.ban != 1:
            users[int(post_author.id)] = post_author.name
            posts.append(post)

    return render_template('post/list.html', posts=posts, users=users)

@post.route('/post/<int:id>', methods=['GET', 'POST'])
def view(id):
    post = Post.query.filter_by(id=id).first()
    if post:
        if request.method == "POST":
            if current_user.ban != 1:
                author_id = current_user.id
                content = request.form.get('content')
                
                if len(content) > 100+1:
                    flash('Максимальная длина комментария: 100 символов')
                    return redirect(url_for("post.view", id=id))

                if content.replace(" ", "") != "":
                    new_user = Comment(post_id=id, author_id=author_id, content=content)
                    post.active = datetime.datetime.now()

                    db.session.add(new_user)
                    db.session.commit()

            return redirect(url_for("post.view", id=id))
        else:
            post_author = User.query.filter_by(id=post.author_id).first()

            if post_author.ban == 1 and current_user.admin < 1:
                return redirect(url_for("main.profile") + "/" + str(post_author.id))
            else:
                post_comments = Comment.query.filter_by(post_id=post.id)
                comments = []
                for comment in post_comments:
                    comment_author = User.query.filter_by(id=comment.author_id).first()
                    if comment and comment_author.ban != 1 or current_user.admin > 0:
                        comments.append([comment_author.name, comment_author.admin, comment.content, comment_author.id, comment_author.ban])
                return render_template('post/view.html', post=post, user=post_author, comments=reversed(comments))
    else:
        return render_template('error/not_found.html', message="Пост не найден.")

@post.route('/post/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    post = Post.query.filter_by(id=id).first()
    if post:
        if post.author_id == current_user.id:
            if request.method == "POST":
                title = request.form.get('title')
                content = request.form.get('content')

                other_post = Post.query.filter_by(title=title).first()

                if other_post and post.id != other_post.id and title == other_post.title:
                    flash('Пост с таким же названием уже существует.')
                    return redirect(url_for('post.edit', id=id))

                if len(title) > 30+1:
                    flash('Максимальная длина заголовка: 30 символов')
                    return redirect(url_for('post.edit', id=id))
                elif len(content) > 1500+1:
                    flash('Максимальная длина содержания: 1500 символов')
                    return redirect(url_for('post.edit', id=id))

                post.title = title
                post.content = content
                post.active = datetime.datetime.now()

                db.session.commit()
                return redirect(url_for("post.view", id=id))
            else:
                return render_template('post/edit.html', post=post)
        else:
            return redirect(url_for("post.view", id=id))
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

            if len(title) > 30+1:
                flash('Максимальная длина заголовка: 30 символов')
                return redirect(url_for('post.create'))
            elif len(content) > 1500+1:
                flash('Максимальная длина содержания: 1500 символов')
                return redirect(url_for('post.create'))

            new_post = Post(author_id=current_user.id, title=title, content=content, active=datetime.datetime.now())

            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for('main.profile'))
        else:
            flash('Ваш аккаунт заблокирован, вы не можете создавать публикации.')
            return redirect(url_for('post.create'))
    else:
        return render_template('post/create.html')