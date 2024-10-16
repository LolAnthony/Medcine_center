from django.urls import path

from empProfile import views

urlpatterns = [
    path('', views.empProfile, name='empProfile'),
]
