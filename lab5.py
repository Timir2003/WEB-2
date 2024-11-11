from flask import Blueprint, render_template, request, redirect, session, flash
lab5 = Blueprint('lab5', __name__)
import psycopg2

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')

@lab5.route('/lab5/list')
def list_articles():
    return 'Страница со списком статей'

@lab5.route('/lab5/create')
def create_article():
    return 'Страница для создания статей'

@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template ('/lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error="Заполните все поля")
    
    conn = psycopg2.connect(dbname="WEB", user="postgres", password="postgres", host="127.0.0.1"
        )
    cur = conn.cursor()
    cur.execute("SELECT login FROM users WHERE login='{login}'")
    if cur.fetchone():
        cur.close()
        conn.close()
        return render_template('lab5/register.html', error="Такой пользователь уже существует")
    
    cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}', '{password}');")
    conn.commit()
    cur.close()
    conn.close()
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/success')
def success():
    return render_template('/lab5/success.html')