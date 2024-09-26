from flask import Blueprint, render_template
lab2 = Blueprint('lab2', __name__)


@lab2.route("/lab2/example")
def example():
    name, course, group, num_lab = 'Остапенко Тимур', 'Курс 3', 'ФБИ-23', 2
    fruits = [
        {'name':'яблоки', 'price': 100},
        {'name':'груши', 'price': 120},
        {'name':'апельсины', 'price': 80},
        {'name':'мандарины', 'price': 95}, 
        {'name':'манго', 'price': 321},
    ]

    book = [
        {'autor':'Александр Островский', 'name_book': 'Гроза', 'style': 'Драма', 'num_pag': 60},
        {'autor':'Михаил Булгаков', 'name_book': 'Морфий', 'style': 'Повесть', 'num_pag': 31},
        {'autor':'Александр Пушкин', 'name_book': 'Капитанская дочка', 'style': 'Роман', 'num_pag': 130},
        {'autor':'Максим Горький', 'name_book':  'На дне', 'style': 'Драма', 'num_pag': 70},
        {'autor':'Федор Достоквский', 'name_book': 'Братья Карамазовы', 'style': 'Классика', 'num_pag': 1140},
        {'autor':'Федор Достоквский', 'name_book': 'Преступление и наказание', 'style': 'Социальная проза', 'num_pag': 680},
        {'autor':'Алесандр Куприн', 'name_book': 'Гранатовый браслет', 'style': 'Повесть', 'num_pag': 60},
        {'autor':'Александр Пушкин', 'name_book': 'Евгений Онегин', 'style': 'Классика', 'num_pag': 100},
        {'autor':'Иван Тургенев', 'name_book': 'Отцы и дети ', 'style': 'Классика', 'num_pag': 240},
        {'autor':'Алесандр Куприн', 'name_book': 'Олеся', 'style': 'Классика', 'num_pag': 90},
    ]

    return render_template ('example.html', name=name, course=course, group=group, 
                            num_lab=num_lab, fruits=fruits, book=book)



@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')


@lab2.route('/lab2/dessert')
def dessert():
    return render_template('dessert.html')
