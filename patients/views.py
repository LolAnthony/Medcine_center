from django.db import connection
from django.shortcuts import render, redirect


def get_permissions(request):
    with connection.cursor() as cursor:
        req_id = request.session.get('id')
        cursor.execute('SELECT `Должность_id` FROM `персонал` WHERE id=%s', (req_id,))
        emp_stat = cursor.fetchone()
    return emp_stat[0]


def get_patient_info(request, *, pat):
    if request.GET.get('pat') or pat:
        pat_i = request.GET.get('pat') or pat
        with connection.cursor() as cursor:
            cursor.execute('SELECT `Фамилия`, `Имя`, `Отчество`, `Дата_рождения`, `Пол`, `id` '
                           'FROM `пациент` '
                           'WHERE id=%s',
                           (pat_i,))
            patient = cursor.fetchone()
        return patient
    else:
        return None


def patients(request, message=''):
    if request.session.get('id'):
        with connection.cursor() as cursor:
            query = 'SELECT `Фамилия`, `Имя`, `Отчество`, `Дата_рождения`, `id` FROM `пациент`'
            if request.GET.get('find'):
                query += ' WHERE CONCAT(`Фамилия`, " ", `Имя`, " ", `Отчество`, " ", `Дата_рождения`) LIKE %s'
                cursor.execute(query, ('%' + request.GET.get('find') + '%',))
            else:
                cursor.execute(query)
            patients_list = cursor.fetchall()
        return render(request, 'patients/list.html',
                      {'title': 'Пациенты', 'patients': patients_list, 'message': message})
    else:
        return redirect('login')


def new_patient(request):
    if request.session.get('id'):
        emp_stat = get_permissions(request)
        if emp_stat != 1:
            return redirect('patients', message='Добавлять пациентов может только врач')
        if all(request.POST.get(field) for field in ['Фамилия', 'Имя', 'Отчество', 'Дата_рождения', 'Пол']):
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO `пациент` (`Фамилия`, `Имя`, `Отчество`, `Дата_рождения`, `Пол`) '
                               'VALUES (%s, %s, %s, %s, %s)',
                               (request.POST.get('Фамилия'), request.POST.get('Имя'),
                                request.POST.get('Отчество'), request.POST.get('Дата_рождения'),
                                request.POST.get('Пол')))
                ins_patient = cursor.lastrowid
            return redirect('check_patient', ins_patient)
        else:
            return render(request, 'patients/new_patient.html', {'title': 'Добавить пациента'})
    else:
        return redirect('login')


def check_patient(request, pat):
    if request.session.get('id'):
        patient = get_patient_info(request, pat=pat)
        if not patient:
            return redirect('patients')
        return render(request, 'patients/patient_info.html', {'title': 'Пациент', 'patient': patient})
    else:
        return redirect('login')


def open_reception(request, *, pat=None):
    if request.session.get('reception'):
        return redirect('patients', message='Завершите свой предыдущий прием, чтобы начать следующий')
    if request.session.get('id'):
        if get_permissions(request) != 1:
            return redirect('patients', message='Начинать прием может только врач')
        patient = get_patient_info(request, pat=pat)
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO `прием` '
                           '(`Дата_приема`, `Пациент_id`, `Персонал_id`) '
                           'VALUES (CURRENT_DATE(), %s, %s)', (pat, request.session.get('id')))
            rec_id = cursor.lastrowid
        request.session['reception'] = rec_id
        return redirect('reception')
    else:
        return redirect('patients')


def close_reception(request):
    request.session.pop('reception')
    return redirect('patients')


def get_allergy(request, *, pat):
    if request.GET.get('pat') or pat:
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT a.`Комментарий`, b.`Причина` FROM `аллергия_пациент` a INNER JOIN `аллергия` b ON a.`аллергия_id` = b.`id` WHERE a.`пациент_id`=%s',
                (request.GET.get('pat') or pat,))
            pat_allergies = cursor.fetchall()
        return pat_allergies
    else:
        return None


def get_def_symptoms():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM `симптом`')
        def_symptoms = cursor.fetchall()
    return def_symptoms


def get_def_diagnosis():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM `диагноз`')
        def_diagnosis = cursor.fetchall()
    return def_diagnosis


def get_symptoms(request, rec):
    with connection.cursor() as cursor:
        cursor.execute('SELECT s.`Название`, pr.`Комментарий` '
                       'FROM `прием_симптомы` pr '
                       'JOIN `симптом` s on s.`id`=pr.`Симптом_id` '
                       'WHERE pr.`Прием_id`=%s ', (rec,))
        symptoms = cursor.fetchall()
    return symptoms


def get_diagnosis(request, rec):
    with connection.cursor() as cursor:
        cursor.execute('SELECT d.`Название`, pr.`Комментарий` '
                       'FROM `дата_диагноза` pr '
                       'JOIN `диагноз` d on d.`id`=pr.`Диагноз_id` '
                       'WHERE pr.`Прием_id`=%s ', (rec,))
        diagnosis = cursor.fetchall()
    return diagnosis


def get_all_allergies(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM `аллергия`')
        allergy_list = cursor.fetchall()
        return allergy_list


def patient_allergies(request, pat):
    if request.method == 'POST':
        patient_id = request.GET.get('pat') or pat
        allergy_id = request.POST.get('allergy_id')
        comment = request.POST.get('comment')
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO `аллергия_пациент` (`пациент_id`, `аллергия_id`, `Комментарий`) '
                           'VALUES (%s, %s, %s)', (patient_id, allergy_id, comment))
        return redirect('patients_allergies', pat=patient_id)
    else:
        patient_allergies_list = get_allergy(request, pat=pat)
        allergy_list = get_all_allergies(request)
        return render(request, 'patients/patient_allergies.html', {
            'title': 'Аллергии пациента',
            'patient_allergies': patient_allergies_list,
            'pat_id': pat,
            'allergy_list': allergy_list,
        })


def reception(request):
    if not request.session.get('reception'):
        return redirect('patients', message='Прием не был начат, либо завершен')
    emp_stat = get_permissions(request)
    if emp_stat != 1:
        return redirect('login')
    if request.method == 'POST':
        if request.POST.get('symptom_id'):
            symptom_id = request.POST.get('symptom_id')
            symptom_comment = request.POST.get('symptom_comment')
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO `прием_симптомы` (`Симптом_id`, `Прием_id`, `Комментарий`) '
                               'VALUES (%s, %s, %s)',
                               (symptom_id, str(request.session.get('reception')), symptom_comment))
        if request.POST.get('diagnos_id'):
            diagnos_id = request.POST.get('diagnos_id')
            diagnos_comment = request.POST.get('diagnos_comment')
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO `дата_диагноза` (`Прием_id`, `Диагноз_id`, `Комментарий`) '
                               'VALUES (%s, %s, %s)',
                               (str(request.session.get('reception')), diagnos_id, diagnos_comment))
    with connection.cursor() as cursor:
        cursor.execute('SELECT `Пациент_id` FROM `прием` WHERE `id`=%s', (str(request.session.get('reception')),))
        pat_id = cursor.fetchone()[0]
        patient = get_patient_info(request, pat=pat_id)
        cursor.execute(
            'SELECT p.`Дата_приема`, pers.`Фамилия`, pers.`Имя`, pers.`Отчество`, otd.`Название`, p.`id` FROM `прием` p '
            'JOIN `персонал` pers ON pers.id=p.`Персонал_id` '
            'JOIN `отделение` otd ON otd.id=pers.`Отделение_id` '
            'WHERE `Пациент_id`=%s AND p.`id` != %s',
            (pat_id, str(request.session.get('reception'))))
        receptions = cursor.fetchall()
    symptoms = get_symptoms(request, str(request.session.get('reception')))
    diagnosis = get_diagnosis(request, str(request.session.get('reception')))
    def_diagnosis = get_def_diagnosis()
    def_symptoms = get_def_symptoms()
    return render(request, 'patients/reception.html', {'title': 'Прием', 'receptions': receptions, 'patient': patient,
                                                       'diagnosis': diagnosis, 'symptoms': symptoms,
                                                       'def_diagnosis': def_diagnosis, 'def_symptoms': def_symptoms})


def check_previous_reception(request, rec_id):
    with connection.cursor() as cursor:
        cursor.execute('SELECT `Пациент_id` FROM `прием` WHERE `id`=%s', (rec_id,))
        pat_id = cursor.fetchone()[0]
        cursor.execute(
            'SELECT p.`Дата_приема`, pers.`Фамилия`, pers.`Имя`, pers.`Отчество`, otd.`Название` FROM `прием` p '
            'JOIN `персонал` pers ON pers.id=p.`Персонал_id` '
            'JOIN `отделение` otd ON otd.id=pers.`Отделение_id` '
            'WHERE p.`id`=%s', (rec_id,))
        reception = cursor.fetchone()
        patient = get_patient_info(request, pat=pat_id)
    symptoms = get_symptoms(request, rec_id)
    diagnosis = get_diagnosis(request, rec_id)
    return render(request, 'patients/old_reception.html', {'title': 'Прошлый прием', 'patient': patient,
                                                           'diagnosis': diagnosis, 'symptoms': symptoms,
                                                           'reception': reception})


def close_reception(request):
    request.session.pop('reception')
    return redirect('patients', message='Прием закрыт')
