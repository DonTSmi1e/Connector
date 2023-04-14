from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

from .models import User
from .models import Post
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile/profile.html', user=current_user, posts=Post.query.filter_by(author_id=current_user.id))

@main.route('/profile/<int:id>')
def profile_id(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return render_template('profile/profile.html', user=user, posts=Post.query.filter_by(author_id=user.id))
    else:
        return render_template('profile/profile_notfound.html')

@main.route('/profile/settings', methods=['GET', 'POST'])
@login_required
def profile_settings():
    if request.method == 'POST':
        new_description = request.form.get('description')
        current_user.description = new_description
        db.session.commit()
        flash("Описание успешно изменено.")
    return render_template('profile/profile_settings.html')