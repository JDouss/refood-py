from email.policy import default

from django import forms
from django.db import connections
from django.utils import timezone
from .models import AlEnt

def get_alimentos_entrada():
    return AlEnt.objects.values_list('id_market', 'description')


class MenuPrincipalForm(forms.Form):
    TIPO_CHOICES = [
        ('entradas', 'Entradas'),
        ('salidas', 'Salidas'),
    ]
    tipo_form = forms.ChoiceField(widget=forms.Select(attrs={'id': 'id_menu_principal', 'name': 'tipo_formulario'}),
                                 choices=TIPO_CHOICES)

class EntradasForm(forms.Form):
    nombre_alimento = forms.ChoiceField(widget=forms.Select(attrs={'id': 'id_nombre_alimento_entrada'}),
                                        choices=['Lasaña','Lentejas','Arroz'],
                                      required=False)
    donante = forms.ChoiceField(widget=forms.Select(attrs={'id': 'id_build_eff'}),
                                choices=['D1','D2','D3'],
                                  required=False)
    peso = forms.CharField(widget=forms.TextInput(attrs={'id': 'peso'}), required=True)
    fecha_llegada = forms.DateField(widget=forms.SelectDateWidget(attrs={'id': 'date_beg'}),
                                    required=False,
                                    )
    nombre_alimento = forms.ChoiceField(widget=forms.Select(attrs={'id': 'id_nombre_alimento_entrada'}),
                                        choices=['Comida Preparada', 'Fruta y verdura'],
                                        required=False)

class SalidasForm(forms.Form):
    building_type = forms.ChoiceField(widget=forms.Select(attrs={'id': 'id_build_type'}), choices=['A'],
                                      required=False)
    dimension = forms.CharField(widget=forms.TextInput(attrs={'id': 'dimension'}),
                                required=False)
    eff_class = forms.ChoiceField(widget=forms.Select(attrs={'id': 'id_build_eff'}), choices=['A'],
                                  required=False)
    holiday_begin = forms.DateField(widget=forms.SelectDateWidget(attrs={'id': 'date_beg'}),
                                    required=False)
    holiday_end = forms.DateField(widget=forms.SelectDateWidget(attrs={'id': 'date_end'}),
                                  required=False)
