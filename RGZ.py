from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session,  current_app, Flask, flash, jsonify
from functools import wraps
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path

RGZ = Blueprint('RGZ', __name__)

ADMIN_USER = 'Timur'

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        try:
            conn = psycopg2.connect(
                dbname="WEB", 
                user="postgres", 
                password="Super0925!", 
                host="127.0.0.1"
            )
            cur = conn.cursor(cursor_factory=RealDictCursor)
        except Exception as e:
            print(f"Ошибка подключения к PostgreSQL: {e}")
            return None, None
    else:
        try:
            dir_path = path.dirname(path.realpath(__file__))
            db_path = path.join(dir_path, "database.db")
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
        except Exception as e:
            print(f"Ошибка подключения к SQLite: {e}")
            return None, None

    return conn, cur

def db_close(conn, cur):
    if conn and cur:
        conn.commit()
        cur.close()
        conn.close()


@RGZ.route('/RGZ/login')
def log():
    return render_template('/RGZ/login.html')

@RGZ.route('/RGZ/logout')
def logoute():
    session.pop('login', None)
    return render_template('/RGZ/login.html')

@RGZ.route('/RGZ/register')
def reg():
    return render_template('/RGZ/register.html')

@RGZ.route('/RGZ/')
def lab():
    conn, cur = db_connect()
    if conn is None or cur is None:
        return render_template('/RGZ/RGZ.html', authors=[], genres=[], page_count=[])

    try:
        # Получаем уникальных авторов, жанры и количество страниц из базы данных
        cur.execute("SELECT DISTINCT author FROM books")
        authors = [row['author'] for row in cur.fetchall()]

        cur.execute("SELECT DISTINCT genre FROM books")
        genres = [row['genre'] for row in cur.fetchall()]

        cur.execute("SELECT DISTINCT page_count FROM books")
        page_count = [row['page_count'] for row in cur.fetchall()]

        # Получаем все книги
        cur.execute("SELECT * FROM books;")
        books = cur.fetchall()  # Получаем список книг

    except Exception as e:
        db_close(conn, cur)
        return render_template('/RGZ/RGZ.html', authors=[], genres=[], page_count=[], books=[], error=str(e))

    db_close(conn, cur)
    return render_template('/RGZ/RGZ.html', authors=authors, genres=genres, page_count=page_count, books=books)

@RGZ.route('/api/books', methods=['GET'])
def get_books():
    # Проверка авторизации
    if 'login' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    author = request.args.get('author', '')
    genre = request.args.get('genre', '')
    pages_from = request.args.get('pages_from', '')
    pages_to = request.args.get('pages_to', '')
    page = int(request.args.get('page', 1))  # Текущая страница
    limit = 20  # Количество книг на странице
    offset = (page - 1) * limit  # Смещение

    conn, cur = db_connect()
    if conn is None or cur is None:
        return jsonify({"error": "Database connection error"}), 500

    conditions = []
    params = []

    if author:
        conditions.append("author = %s" if current_app.config['DB_TYPE'] == 'postgres' else "author = ?")
        params.append(author)

    if genre:
        conditions.append("genre = %s" if current_app.config['DB_TYPE'] == 'postgres' else "genre = ?")
        params.append(genre)

    if pages_from:
        conditions.append("page_count >= %s" if current_app.config['DB_TYPE'] == 'postgres' else "page_count >= ?")
        params.append(int(pages_from))

    if pages_to:
        conditions.append("page_count <= %s" if current_app.config['DB_TYPE'] == 'postgres' else "page_count <= ?")
        params.append(int(pages_to))

    query = "SELECT id, cover_image, title, author, page_count AS pages, publisher, genre FROM books WHERE TRUE"
    
    if conditions:
        query += " AND " + " AND ".join(conditions)
    # Получаем общее количество книг
    count_query = "SELECT COUNT(*) FROM books WHERE TRUE"
    if conditions:
        count_query += " AND " + " AND ".join(conditions)

    # Добавляем LIMIT и OFFSET
    if current_app.config['DB_TYPE'] == 'postgres':
        query += " LIMIT %s OFFSET %s"
    else:
        query += " LIMIT ? OFFSET ?"

    try:
        # Выполнение запроса для получения общего количества книг
        cur.execute(count_query, params)
        total_count = cur.fetchone()[0]  # Общее количество книг

        # Получаем книги с пагинацией
        params.append(limit)
        params.append(offset)

        cur.execute(query, params)
        books = cur.fetchall()
        
        # Преобразование результата в список словарей
        books_list = [dict(book) for book in books]
    except Exception as e:
        db_close(conn, cur)
        return jsonify({"error": f"Ошибка выполнения запроса: {str(e)}"}), 500

    db_close(conn, cur)

    total_pages = (total_count + limit - 1) // limit  # Общее количество страниц
    return jsonify({"books": books_list, "total_pages": total_pages})

@RGZ.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')

    if not (login and password):
        return jsonify({"error": "Заполните все поля"}), 400

    conn, cur = db_connect()
    if conn is None or cur is None:
        return jsonify({"error": "Ошибка подключения к базе данных"}), 500

    try:
        cur.execute("SELECT login FROM users WHERE login=%s;" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT login FROM users WHERE login=?;", (login,))
        if cur.fetchone():
            return jsonify({"error": "Такой пользователь уже существует"}), 400

        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);" if current_app.config['DB_TYPE'] == 'postgres' else "INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))
        conn.commit()
    except Exception as e:
        db_close(conn, cur)
        return jsonify({"error": f"Ошибка выполнения запроса: {e}"}), 500

    db_close(conn, cur)

    return jsonify({"message": "Регистрация прошла успешно"}), 201

@RGZ.route('/RGZ/manage_books')
def manage_books():
    conn, cur = db_connect()
    if conn is None or cur is None:
        return render_template('/RGZ/admin/manage_books.html', authors=[], genres=[], page_count=[], books=[], error="Ошибка подключения к базе данных")

    try:
        # Получаем уникальных авторов из базы данных
        cur.execute("SELECT DISTINCT author FROM books")
        authors = [row['author'] for row in cur.fetchall()]

        # Получаем уникальные жанры из базы данных
        cur.execute("SELECT DISTINCT genre FROM books")
        genres = [row['genre'] for row in cur.fetchall()]

        # Получаем уникальные количества страниц из базы данных
        cur.execute("SELECT DISTINCT page_count FROM books")
        page_count = [row['page_count'] for row in cur.fetchall()]

        # Получаем все книги
        cur.execute("SELECT * FROM books;")
        books = cur.fetchall()  # Получаем список книг

    except Exception as e:
        db_close(conn, cur)
        return render_template('/RGZ/admin/manage_books.html', authors=[], genres=[], page_count=[], books=[], error=str(e))

    db_close(conn, cur)

    return render_template('/RGZ/admin/manage_books.html', authors=authors, genres=genres, page_count=page_count, books=books)

@RGZ.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')

    if not (login and password):
        return jsonify({"error": "Заполните поля"}), 400

    conn, cur = db_connect()
    if conn is None or cur is None:
        return jsonify({"error": "Ошибка подключения к базе данных"}), 500

    try:
        cur.execute("SELECT * FROM users WHERE login=%s;" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT * FROM users WHERE login=?;", (login,))
        user = cur.fetchone()

        if not user or not check_password_hash(user['password'], password):
            return jsonify({"error": "Логин и/или пароль неверны"}), 401

        session['login'] = user['login']
        session['role'] = 'admin' if user['login'] == ADMIN_USER else 'user'
    except Exception as e:
        db_close(conn, cur)
        return jsonify({"error": f"Ошибка выполнения запроса: {e}"}), 500

    db_close(conn, cur)

    redirect_url = url_for('RGZ.manage_books') if session['role'] == 'admin' else url_for('RGZ.lab')

    return jsonify({"message": "Вы успешно вошли в систему!", "redirect": redirect_url}), 200

@RGZ.route('/api/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return jsonify({"message": "Вы вышли из системы!"}), 200

@RGZ.route('/api/admin/books', methods=['GET'])
def get_admin_books():
    if 'login' not in session or session['role'] != 'admin':
        return jsonify({"error": "Unauthorized"}), 401

    author = request.args.get('author', '')
    genre = request.args.get('genre', '')
    pages_from = request.args.get('pages_from', '')
    pages_to = request.args.get('pages_to', '')

    conn, cur = db_connect()
    if conn is None or cur is None:
        return jsonify({"error": "Database connection error"}), 500

    conditions = []
    params = []

    if author:
        conditions.append("author = %s" if current_app.config['DB_TYPE'] == 'postgres' else "author = ?")
        params.append(author)

    if genre:
        conditions.append("genre = %s" if current_app.config['DB_TYPE'] == 'postgres' else "genre = ?")
        params.append(genre)

    if pages_from:
        conditions.append("page_count >= %s" if current_app.config['DB_TYPE'] == 'postgres' else "page_count >= ?")
        params.append(int(pages_from))

    if pages_to:
        conditions.append("page_count <= %s" if current_app.config['DB_TYPE'] == 'postgres' else "page_count <= ?")
        params.append(int(pages_to))

    query = "SELECT id, cover_image, title, author, page_count AS pages, publisher, genre FROM books WHERE TRUE"
    
    if conditions:
        query += " AND " + " AND ".join(conditions)

    try:
        cur.execute(query, params)
        books = cur.fetchall()
        
        # Преобразование результата в список словарей
        books_list = [dict(book) for book in books]  # Преобразуем каждую строку в словарь
    except Exception as e:
        db_close(conn, cur)
        return jsonify({"error": f"Ошибка выполнения запроса: {str(e)}"}), 500
    
    db_close(conn, cur)

    return jsonify({"books": books_list})

@RGZ.route('/api/admin/books', methods=['POST'])
def add_admin_book():
    if 'login' not in session or session['role'] != 'admin':
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    genre = data.get('genre')
    pages = data.get('pages')
    publisher = data.get('publisher')
    cover_image = data.get('cover_image')

    if not all([title, author, genre, pages, publisher, cover_image]):
        return jsonify({"error": "Missing fields"}), 400

    conn, cur = db_connect()
    if conn is None or cur is None:
        return jsonify({"error": "Database connection error"}), 500

    query = """
    INSERT INTO books (title, author, genre, page_count, publisher, cover_image)
    VALUES (%s, %s, %s, %s, %s, %s);
    """ if current_app.config['DB_TYPE'] == 'postgres' else """
    INSERT INTO books (title, author, genre, page_count, publisher, cover_image)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    
    try:
        cur.execute(query, (title, author, genre, pages, publisher, cover_image))
        conn.commit()
    except Exception as e:
        db_close(conn, cur)
        return jsonify({"error": f"Ошибка выполнения запроса: {e}"}), 500

    db_close(conn, cur)

    return jsonify({"message": "Book added successfully"}), 201

@RGZ.route('/api/book', methods=['POST'])
def add_book():
    # Проверка авторизации
    if 'login' not in session or session['login'] != ADMIN_USER:
        return jsonify({"error": "Unauthorized"}), 401

    # Получение данных из запроса
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    genre = data.get('genre')
    page_count = data.get('page_count')
    publisher = data.get('publisher')
    cover_image = data.get('cover_image')

    # Проверка наличия всех необходимых полей
    if not all([title, author, genre, page_count, publisher, cover_image]):
        return jsonify({"error": "Заполните все поля"}), 400

    # Подключение к базе данных
    conn, cur = db_connect()
    if conn is None or cur is None:
        return jsonify({"error": "Ошибка подключения к базе данных"}), 500

    # Определение типа базы данных
    db_type = current_app.config['DB_TYPE']
    placeholder = '%s' if db_type == 'postgres' else '?'

    try:
        # Вставка новой книги в базу данных
        cur.execute(
            f"""
            INSERT INTO books (title, author, genre, page_count, publisher, cover_image)
            VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
            """,
            (title, author, genre, page_count, publisher, cover_image)
        )
        conn.commit()  # Фиксация изменений
    except Exception as e:
        # Обработка ошибок выполнения запроса
        return handle_db_error(e, conn, cur)

    # Закрытие соединения с базой данных
    db_close(conn, cur)

    return jsonify({"message": "Книга добавлена успешно!"}), 201

def handle_db_error(error, conn, cur):
    """Обработка ошибок базы данных и закрытие соединения."""
    db_close(conn, cur)
    return jsonify({"error": f"Ошибка выполнения запроса: {str(error)}"}), 500

@RGZ.route('/RGZ/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    conn, cur = db_connect()
    if conn is None or cur is None:
        return "Ошибка подключения к базе данных", 500

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        pages = request.form['page_count'] 
        publisher = request.form['publisher']
        cover_image = request.form['cover_image']

        try:
            cur.execute("""
                UPDATE books 
                SET title=%s, author=%s, genre=%s, page_count=%s, publisher=%s, cover_image=%s 
                WHERE id=%s;
            """ if current_app.config['DB_TYPE'] == 'postgres' else """
                UPDATE books 
                SET title=?, author=?, genre=?, page_count=?, publisher=?, cover_image=? 
                WHERE id=?;
            """, (title, author, genre, pages, publisher, cover_image, book_id))
            conn.commit()
        except Exception as e:
            db_close(conn, cur)
            return f"Ошибка обновления книги: {e}", 500

        db_close(conn, cur)

        flash('Книга успешно обновлена!')
        return redirect(url_for('RGZ.manage_books'))

    try:
        cur.execute("SELECT id, cover_image, title, author, page_count AS pages, publisher, genre FROM books WHERE id = %s" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT id, cover_image, title, author, page_count AS pages, publisher, genre FROM books WHERE id = ?", (book_id,))
        book = cur.fetchone()
    except Exception as e:
        db_close(conn, cur)
        return f"Ошибка получения данных книги: {e}", 500

    db_close(conn, cur)

    if book is None:
        return "Книга не найдена", 404

    return render_template('/RGZ/admin/edit_book.html', book=book)

@RGZ.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    if 'login' not in session or session['login'] != ADMIN_USER:
        return jsonify({"error": "Unauthorized"}), 401
    
    conn, cur = db_connect()
    if conn is None or cur is None:
        return jsonify({"error": "Database connection error"}), 500

    try:
        cur.execute("DELETE FROM books WHERE id=%s;" if current_app.config['DB_TYPE'] == 'postgres' else "DELETE FROM books WHERE id=?;", (book_id,))
        conn.commit()
    except Exception as e:
        db_close(conn, cur)
        return jsonify({"error": f"Ошибка выполнения запроса: {e}"}), 500

    db_close(conn, cur)

    return jsonify({"message": "Book deleted successfully"}), 204
