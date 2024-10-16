from django.db import connection
from django.shortcuts import render, redirect


def empProfile(request):
    if request.session.get('id'):
        req_id = request.session.get('id')
        with connection.cursor() as cursor:
            cursor.execute('SELECT p.`Фамилия`, p.`Имя`, p.`Отчество`, p.`Телефон`, otd.`Название`, dolg.`Название` '
                           'FROM `персонал` p '
                           'JOIN `отделение` otd on p.`Отделение_id`=otd.id '
                           'JOIN `должность` dolg on p.`Должность_id`=dolg.`id` '
                           'WHERE p.id = %s', (req_id,))
            raw = cursor.fetchall()[0]
        context = {'title': 'Профиль', 'Фамилия': raw[0], 'Имя': raw[1], 'Отчество': raw[2], 'Телефон': raw[3], 'Отделение': raw[4], 'Должность': raw[5]}
        return render(request, 'empProfile/profile.html', context)
    else:
        return redirect('login')
