from flask import Blueprint, render_template, request, redirect, session, flash, current_app
lab8 = Blueprint('lab8', __name__)



@lab8.route('/lab8/')
def index():
    return render_template('lab8/index.html')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    return render_template('lab8/login.html')

@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    return render_template('lab8/register.html')

@lab8.route('/lab8/articles', methods=['GET'])
def articles():
    return render_template('lab8/articles.html')

@lab8.route('/lab8/create', methods=['GET', 'POST'])
def create():
    return render_template('lab8/create.html')