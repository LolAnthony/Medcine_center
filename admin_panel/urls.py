from django.urls import path

from admin_panel import views

urlpatterns = [
    path('', views.admin_panel, name='admin_panel'),
    path('add_symptom/', views.add_symptom, name='add_symptom'),
    path('add_diagnos/', views.add_diagnos, name='add_diagnos'),
    path('add_otd/', views.add_otd, name='add_otd'),
    path('add_pers/', views.add_pers, name='add_pers'),
]
