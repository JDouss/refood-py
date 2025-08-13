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
    TIPO_ALIMENTO = [
        (1, 'Lasaña'),
        (2, 'Lentejas'),
        (3, 'Arroz'),
    ]
    nombre_alimento = forms.ChoiceField(
        widget=forms.Select(attrs={
            'id': 'id_nombre_alimento_entrada',
            'class': 'form-control'
        }),
        choices=TIPO_ALIMENTO,
        required=True
    )
    peso = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        }),
        required=True
    )
    donante = forms.ChoiceField(widget=forms.Select(attrs={'id': 'id_donante'}),
                                choices=['D1','D2','D3'],
                                  required=True)
    fecha_llegada = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'id': 'date_beg',
            }
        ),
        required=True,
        initial=timezone.now,
    )

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
