from django.db import connection
from django.shortcuts import render


def admin_panel(request):
    return render(request, 'admin_panel/admin_panel.html')


def add_symptom(request):
    message = ''
    if request.method == 'POST':
        symptom = request.POST.get('symptom_name')
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO `симптом` (`Название`) '
                           'VALUES (%s)', (symptom,))
        message = 'Успешно добавлен класс симптома'
    return render(request, 'admin_panel/add_symptom.html', {'message': message})


def add_diagnos(request):
    message = ''
    if request.method == 'POST':
        diagnos = request.POST.get('diagnosis_name')
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO `диагноз` (`Название`) '
                           'VALUES (%s)', (diagnos,))
        message = 'Успешно добавлен класс диагноза'
    return render(request, 'admin_panel/add_diagnosis.html', {'message': message})


def add_otd(request):
    message = ''
    if request.method == 'POST':
        otd = request.POST.get('otd')
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO `отделение` (`Название`) '
                           'VALUES (%s)', (otd,))
        message = 'Успешно добавлено отделение'
    return render(request, 'admin_panel/add_otd.html', {'message': message})


def add_pers(request):
    message = ''
    if request.method == 'POST':
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        phone = request.POST.get('phone')
        otd_id = request.POST.get('otd_id')
        permissions_id = request.POST.get('permissions_id')
        login_us = request.POST.get('login_us')
        password_us = request.POST.get('password_us')
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO `персонал` (`Фамилия`, `Имя`, `Отчество`, '
                           '`Телефон`, `Отделение_id`, `Должность_id`, `Логин`, '
                           '`Пароль`) '
                           'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (last_name, first_name, middle_name,
                                                                       phone, otd_id, permissions_id, login_us,
                                                                       password_us))
        message = 'Успешно добавлен пользователь'
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM `отделение`')
        otd = cursor.fetchall()
        cursor.execute('SELECT `id`, `Название` FROM `должность`')
        perm = cursor.fetchall()
    return render(request, 'admin_panel/add_pers.html', {'perm': perm, 'otd': otd, 'message': message})
