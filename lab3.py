from flask import Blueprint, render_template, request, make_response, redirect, url_for
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get ('name')
    name = name if name else "Аноним"
    age = request.cookies.get ('age')
    age = age if age else "Неизвестно"
    name_color = request.cookies.get ('name_color')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get ('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get ('age')
    if age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get ('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'coffe':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/cookie')
def cokie():
    resp = make_response(redirect('/lab3'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cokie():
    resp = make_response(redirect('/lab3'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    background_color = request.args.get('background-color')
    font_size = request.args.get('font-size')
    if color:
        resp = make_response(redirect('/lab3/settings'))
        resp.set_cookie('color', color)
        resp.set_cookie('background-color', background_color)
        resp.set_cookie('font-size', font_size)
        return resp
    color = request.cookies.get('color')
    background_color = request.cookies.get('background-color')
    font_size = request.cookies.get('font-size')
    resp = make_response(render_template('lab3/settings.html', color=color, background_color=background_color, font_size=font_size))
    return resp

@lab3.route('/lab3/del_settings')
def del_settings():
    resp = make_response(redirect('/lab3/settings'))
    cookies = request.cookies.keys()
    for cookie in cookies:
        resp.set_cookie(cookie, '', expires=0)
    return resp

products = [
        {"name": "Смартфон A", "price": 500, "brand": "Brand A", "color": "Черный"},
        {"name": "Смартфон B", "price": 700, "brand": "Brand B", "color": "Синий"},
        {"name": "Смартфон C", "price": 300, "brand": "Brand C", "color": "Белый"},
        {"name": "Смартфон D", "price": 900, "brand": "Brand A", "color": "Красный"},
        {"name": "Смартфон E", "price": 400, "brand": "Brand B", "color": "Серый"},
        {"name": "Смартфон F", "price": 600, "brand": "Brand C", "color": "Золотой"},
        {"name": "Смартфон G", "price": 800, "brand": "Brand A", "color": "Зеленый"},
        {"name": "Смартфон H", "price": 200, "brand": "Brand B", "color": "Фиолетовый"},
        {"name": "Смартфон I", "price": 1000, "brand": "Brand C", "color": "Розовый"},
        {"name": "Смартфон J", "price": 550, "brand": "Brand A", "color": "Оранжевый"},
        {"name": "Смартфон K", "price": 750, "brand": "Brand B", "color": "Коричневый"},
        {"name": "Смартфон L", "price": 350, "brand": "Brand C", "color": "Бирюзовый"},
        {"name": "Смартфон M", "price": 950, "brand": "Brand A", "color": "Желтый"},
        {"name": "Смартфон N", "price": 450, "brand": "Brand B", "color": "Серебряный"},
        {"name": "Смартфон O", "price": 650, "brand": "Brand C", "color": "Бронзовый"},
        {"name": "Смартфон P", "price": 850, "brand": "Brand A", "color": "Черный"},
        {"name": "Смартфон Q", "price": 250, "brand": "Brand B", "color": "Синий"},
        {"name": "Смартфон R", "price": 1050, "brand": "Brand C", "color": "Белый"},
        {"name": "Смартфон S", "price": 550, "brand": "Brand A", "color": "Красный"},
        {"name": "Смартфон T", "price": 750, "brand": "Brand B", "color": "Серый"},
    ]

@lab3.route('/lab3/search.html')
def search_products():
    
    min_price = int(request.args.get('min_price', 0))
    max_price = int(request.args.get('max_price', 1000))
    filtered_products = [product for product in products
                        if min_price <= product['price'] <= max_price]
    return render_template('lab3/search.html', products=filtered_products, min_price=min_price, max_price=max_price)

@lab3.route('/lab3/index')
def index():
    return render_template('lab3/index.html', products=products)

@lab3.route('/lab3/form_rzd')
def form_rzd():
    errors = {}
    user = request.args.get ('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get ('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
        
    place = request.args.get ('place')
    if place == '':
        errors['place'] = 'Заполните поле!'
    
    exit = request.args.get ('exit')
    if exit == '':
        errors['exit'] = 'Заполните поле!'
    
    arrival = request.args.get ('arrival')
    if arrival == '':
        errors['arrival'] = 'Заполните поле!'

    date = request.args.get ('date')
    if date == '':
        errors['date'] = 'Заполните поле!'

    return render_template('lab3/form_rzd.html', user=user, age=age, place=place, exit=exit, arrival=arrival, date=date, errors=errors)

@lab3.route('/lab3/ticket')
def ticket():
    user = request.args.get('user')
    exit = request.args.get('exit')
    arrival = request.args.get('arrival')
    date = request.args.get('date')
    underwear = request.args.get('underwear')
    luggage = request.args.get('luggage')
    insurance = request.args.get('insurance')
    price = 0
    age = int(request.args.get('age'))
    if age < 18:
        price = 700
    else:
        price = 1000

    place = request.args.get('place')
    if place == 'side_low':
        price += 100
        place = 'нижняя боковая'
    elif place == 'low':
        price += 100
        place = 'нижняя'
    elif place == 'up':
        price += 0
        place = 'верхняя'
    else:
        price += 0
        place = 'верхняя боковая'

    if request.args.get('underwear') == 'on':
        price += 75
    if request.args.get('luggage') == 'on':
        price += 250
    if request.args.get('insurance') == 'on':
        price += 150

    return render_template('lab3/ticket.html', price=price, user=user, age=age, place=place, exit=exit, arrival=arrival, date=date, underwear=underwear, luggage=luggage, insurance=insurance)