from django.db import connection
from django.shortcuts import render, redirect


def login(request):
    if request.POST and request.POST.get('login', 'password'):
        login_post, password = request.POST.get('login'), request.POST.get('password')
        with connection.cursor() as cursor:
            cursor.execute('SELECT id FROM `персонал` WHERE `Логин` =%s AND `Пароль` = %s',
                           (login_post, password))
            raw = cursor.fetchone()
            if raw:
                request.session['id'] = raw[0]
                return redirect('empProfile')
            else:
                return render(request, 'empAuth/login.html', {'title': 'Вход', 'message': 'Неверные данные, попробуйте снова'})
    else:
        return render(request, 'empAuth/login.html', {'title': 'Вход'})


def logout(request):
    request.session.clear()
    return redirect('login')
