from django.urls import path
from . import views

app_name = 'refood_app'
urlpatterns = [
    path('', views.menu_principal, name='menu_principal'),
    path('redirigir/', views.redirigir_formulario, name='redirigir_formulario'),
    path('entradas/', views.entradas, name='entradas'),
    path('salidas/', views.salidas, name='salidas')
]