from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def start():
    return redirect("/menu", code=302)

@app.route("/menu")
def menu():
    return """
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>

        <h1>web-сервер на flask</h1>
        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
            </ul>
        </nav>
        <footer>
            &copy; Остапенко Тимур, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""

@app.route("/lab1")
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Остапенко Тимур Ростиславович, Лабораторная 1</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <header>
            НГТУ, ФБ, Лабораторная 1
        </header>

        <h1>web-сервер на flask</h1>
        <p>
        Flask — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов-приложений, 
        сознательно предоставляющих лишь самые базовые возможности.
        </p>
        <nav>
            <ul>
                <li><a href="/menu">Меню</a></li>
            </ul>
        </nav>
        <h2>Реализованные роуты</h2>
        <nav>
            <ul>
                <li><a href="/lab1/oak">Дуб</a></li>
                <li><a href="/lab1/student">Студент</a></li>
                <li><a href="/lab1/python">Python</a></li>
                <li><a href="/lab1/SQL">SQL</a></li>
            </ul>
        </nav>
        <footer>
            &copy; Остапенко Тимур, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''

@app.route("/lab1/oak")
def oak():
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="'''+url_for('static', filename='oak.jpg')+'''">
    </body>
</html>
'''

@app.route("/lab1/student")
def student():
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <h1>Остапенко Тимур Ростиславович</h1>
        <img src="'''+url_for('static', filename='NETI.jpg')+'''">
    </body>
</html>
'''

@app.route("/lab1/python")
def python():
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <h1>Преимущества: чем хорош Python</h1>
        <img src="'''+url_for('static', filename='python.jpg')+'''">
        <p>
        Специалисты выделяют массу преимуществ Python — остановимся на ключевых из них.
        <b>Простота синтаксиса, а значит — низкий порог вхождения.</b> 
        Код языка чистый и понятный, без лишних символов и выражений.<br>

        <b>Расширяемость и гибкость.</b> Не зря один из слоганов языка — это «Just Import!» 
        Python можно легко расширить для взаимодействия с другими программными 
        системами или встроить в программы в качестве компонента. Он очень и очень гибкий. 
        Это даёт больше возможностей для использования языка в разных сферах.<br>

        <b>Интерпретируемость и кроссплатформенность.</b> Интерпретатор Python есть для всех 
        популярных платформ и по умолчанию входит в большинство дистрибутивов Linux.<br>

        <b>Стандартизированность.</b> У Python есть единый стандарт для написания кода — Python
        Enhancement Proposal или PEP, благодаря чему язык остаётся читабельным даже при 
        переходе от одного программиста к другому.<br>

        <b>Open Source.</b> У интерпретатора Python открытый код, то есть любой, 
        кто заинтересован в развитии языка, может поучаствовать в его разработке и улучшении.<br>

        <b>Сильное комьюнити и конференции.</b> Вокруг Python образовалось дружественное 
        комьюнити, которое готово прийти на помощь новичку или уже опытному разработчику 
        и разобраться в его проблеме. Во всём мире проходит много мероприятий, где можно 
        познакомиться с коллегами и узнать много нового о применении Пайтона.<br>

        <b>Широта применения.</b> Наиболее широко Python используется в web-разработке, 
        работе с данными, автоматизации бизнес-процессов и геймдеве.<br>

        <b>Востребованность на рынке труда и поддержка гигантами IT-сферы.</b> Python-разработчики востребованы 
        во многих проектах и им несложно найти работу. Разработку на Python ведут в Google, 
        Facebook, Dropbox, Spotify, Quora, Netflix, Microsoft Intel, а в России — «Яндекс», 
        «ВКонтакте» и «Сбербанк». Это серьёзно влияет на статус языка.<br>
        </p>
    </body>
</html>
'''

@app.route("/lab1/SQL")
def SQL():
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <h1>Для чего нужен SQL</h1>
        <img src="'''+url_for('static', filename='SQL.jpg')+'''">
        <p>
            SQL (сокращение от англ. Structured Query Language) — это язык запросов, который применяют, 
            чтобы работать с базами данных, структурированных особым образом. Главные задачи SQL — составлять
            запросы так, чтобы находить среди большого объёма информации ту, что нужна для конкретных целей, 
            сортировать её, структурировать и представлять в наиболее простом и понятном виде.<br>

            Чтобы понять, зачем нужен язык SQL, представьте, что женщина выбирает в интернет-магазине 
            летнее платье жёлтого цвета и хочет уложиться в 5 тысяч рублей. Всего в магазине 10 тысяч платьев. 
            Если просто перебирать их по каталогу, уйдёт несколько часов. Но можно задать в фильтрах настройки
            по категории, сезону, цвету, цене и сразу найти нужные модели. Эти фильтры работают за счёт языка запросов SQL.<br>

            Первый прототип языка SQL представила в 1979 году компания-разработчик Oracle. Сначала это был 
            простейший инструмент для извлечения нужных данных, вроде фильтров в Excel-таблицах. С годами он усложнился, 
            и теперь его применяют в качестве одного из основных инструментов для обработки данных. С помощью SQL можно:
             <ul>
                <li>собирать и хранить данные в виде таблиц;</li>
                <li>изменять их содержимое и структуру;</li>
                <li>объединять данные и выполнять вычисления;</li>
                <li>защищать и распределять доступ.</li>   
            </ul>

            Например, в компании работает 500 сотрудников. 100 из них занимаются продажами и постоянно 
            пользуются CRM, чтобы вносить данные о клиентах: новые договоры, суммы, скидки и контакты. 
            И есть 15 IT-специалистов, которые настраивают, обновляют и меняют структуру CRM, когда это требуется. 
            20 сотрудников бухгалтерии регулярно выгружают из системы данные об оплатах, выставленные 
            счета и акты на подпись. При помощи SQL можно предоставить всем им доступ только к нужной 
            части CRM, чтобы никто случайно не повредил важные данные или элементы кода.
        </p>
    </body>
</html>
'''

@app.route("/lab2/example")
def example():
    return render_template ('example.html')    

