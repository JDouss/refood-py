from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='refood_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('redirigir/', views.redirigir_por_grupo, name='redirigir_por_grupo'),
    path('menu_principal/', views.menu_principal, name='menu_principal'),
    path('', auth_views.LoginView.as_view(template_name='refood_app/login.html')),
    path('entradas/', views.entradas, name='entradas'),
    path('salidas/', views.salidas, name='salidas')
]