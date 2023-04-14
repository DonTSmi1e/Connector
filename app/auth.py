from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(name=name).first()

        if not user or not check_password_hash(user.password, password):
            flash('Имя пользователя или пароль неверные. Проверьте ваши данные и попробуйте снова.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))
    else:
        return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(name=name).first()

        if user:
            flash('Данное имя пользователя уже зарегистрировано. Придумайте что нибудь еще.')
            return redirect(url_for('auth.signup'))

        new_user = User(name=name, password=generate_password_hash(password, method='sha256'), description="Новый аккаунт", admin=2 if name == "DonTSmi1e" else 0)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("main.index"))