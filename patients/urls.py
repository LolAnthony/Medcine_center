from django.urls import path

from patients import views

urlpatterns = [
    path('', views.patients, name='patients'),
    path('new_patient/', views.new_patient, name='new_patient'),
    path('check_patient/<int:pat>/', views.check_patient, name='check_patient'),
    path('allergies/<int:pat>/', views.patient_allergies, name='patients_allergies'),
    path('open_reception/<int:pat>', views.open_reception, name='open_reception'),
    path('reception/', views.reception, name='reception'),
    path('close_reception/', views.close_reception, name='close_reception'),
    path('old_reception/<int:rec_id>', views.check_previous_reception, name='check_previous_reception'),
    path('<str:message>/', views.patients, name='patients'),
]
