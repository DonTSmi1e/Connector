from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from .models import User
from .models import Post
from .models import Comment
from . import db

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def index():
    if current_user.admin == 2:
        return render_template('admin/index.html')
    elif current_user.admin == 1:
        return render_template('admin/index_moderator.html')
    else:
        return redirect(url_for('main.index'))

@admin.route('/admin/utils/<int:id>', methods=['POST'])
@login_required
def utils(id):
    if request.method == "POST":
        if id == 1 and current_user.admin >= 1:
            # Очистить недоступные публикации
            comments = Comment.query.all()
            posts = Post.query.all()
            for comment in comments:
                if not User.query.filter_by(id=comment.author_id).first() or not Post.query.filter_by(id=comment.post_id).first():
                    Comment.query.filter_by(id=comment.id).delete()
            for post in posts:
                if not User.query.filter_by(id=post.author_id).first():
                    Post.query.filter_by(id=post.id).delete()
            db.session.commit()
        if id == 3 and current_user.admin >= 2:
            # Очистить все комментарии
            Comment.query.delete()
            db.session.commit()
        elif id == 5 and current_user.admin >= 2:
            # Разбанить все аккаунты
            for user in User.query.all():
                if user and user.ban == 1:
                    user.ban = 0
                    db.session.commit()
        elif id == 6 and current_user.admin >= 2:
            # Удалить аккаунт **ПО ID**
            User.query.filter_by(id=int(request.form.get("id"))).delete()
            db.session.commit()
        elif id == 7 and current_user.admin >= 2:
            # Удалить пост **ПО ID**
            Post.query.filter_by(id=int(request.form.get("id"))).delete()
            db.session.commit()
        elif id == 8 and current_user.admin >= 1:
            # Забанить аккаунт **ПО ID**
            user = User.query.filter_by(id=int(request.form.get("id"))).first()
            if user.ban == 1 and current_user.admin > user.admin:
                user.ban = 0
            elif user.ban == 0 and current_user.admin > user.admin:
                user.ban = 1
            db.session.commit()
        elif id == 9 and current_user.admin >= 1:
            # Выдать уровень администратора **ПО ID**
            user = User.query.filter_by(id=int(request.form.get("id"))).first()
            if current_user.admin > user.admin or current_user.id == 1:
                user.admin = int(request.form.get("admin"))
            db.session.commit()

        return redirect(url_for('admin.index'))
    else:
        return redirect(url_for('main.index'))
