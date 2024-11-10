from flask import Blueprint, render_template, request, redirect, session, flash
lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')

@lab5.route('/lab5/list')
def list_articles():
    return 'Страница со списком статей'

@lab5.route('/lab5/create')
def create_article():
    return 'Страница для создания статей'

@lab5.route('/lab5/login')
def login():
    return 'Страница входа'

@lab5.route('/lab5/register')
def register():
    return 'Страница регистрации'
