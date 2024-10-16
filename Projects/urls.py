from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('empAuth.urls')),
    path('profile/', include('empProfile.urls')),
    path('patients/', include('patients.urls')),
    path('admin_panel/', include('admin_panel.urls')),
]
