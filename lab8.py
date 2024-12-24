from flask import Blueprint, render_template, request, redirect, session, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import Users, Articles
from flask_login import login_user, login_required, current_user

lab8 = Blueprint('lab8', __name__)




@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/login.html', error='Имя пользователя не должно быть пустым')
    
    if not password_form:
        return render_template('lab8/login.html', error='Пароль не должен быть пустым')

    user = Users.query.filter_by(login = login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember = False)
            return redirect('/lab8/')
        
    return render_template('/lab8/login.html', error = 'Ошибка входа: логин и/или пароль неверный')


@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/register.html', error='Имя пользователя не должно быть пустым')
    
    if not password_form:
        return render_template('lab8/register.html', error='Пароль не должен быть пустым')


    login_exists = Users.query.filter_by(login = login_form).first ()
    if login_exists:
        return render_template('lab8/register.html', error = 'Такой пользователь уже существует')
    
    password_hash = generate_password_hash (password_form)
    new_user =  Users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/lab8/')


@lab8.route('/lab8/list', methods=['GET'])
@login_required
def list_articles():
    return render_template('lab8/articles.html')

@lab8.route('/lab8/create', methods=['GET', 'POST'])
def create():
    return render_template('lab8/create.html')