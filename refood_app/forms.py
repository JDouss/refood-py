from datetime import datetime,timedelta
from email.policy import default

from django import forms
from django.db import connections
from django.utils import timezone
from .models import AlEnt,TipoAl,Donante,Benef

def get_tipos_alimentos():
    return TipoAl.objects.values_list('id', 'nombre_alimento')

def get_donantes():
    return Donante.objects.values_list('id','nombre')

def get_beneficiarios():
    beneficiarios = Benef.objects.filter(activo=1).values_list("id", "id_beneficiario", "nombre_representante")
    return [
        (b[0], f"{b[1]} - {b[2]}")
        for b in beneficiarios
    ]

def get_alimentos_entrada(fecha_llegada: datetime):
    al_entrada = (AlEnt.objects.filter(
        fecha_y_hora_entrada__gt=fecha_llegada
    ).select_related(
        "donante", "tipo_al"
    ).values_list(
        "id", "tipo_al__nombre_alimento", "donante__nombre"
    ))
    return [
        (a[0], f"{a[1]} - {a[2]}")
        for a in al_entrada
    ]


class MenuPrincipalForm(forms.Form):
    TIPO_CHOICES = [
        ('entradas', 'Entradas'),
        ('salidas', 'Salidas'),
    ]
    tipo_form = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'id': 'id_menu_principal', 'name': 'tipo_formulario'
            }
        ),
        choices=TIPO_CHOICES
    )

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
        choices=[],
        required=True
    )
    peso = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control'
            }
        ),
        required=True
    )
    donante = forms.ChoiceField(
        widget=forms.Select(
            attrs={'id': 'id_donante'}),
        choices=[],
        required=True
    )
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

    def __init__(self, *args, fecha_llegada=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Rellenar choices dinámicamente en cada instancia del formulario
        self.fields['nombre_alimento'].choices = get_tipos_alimentos()
        self.fields['donante'].choices = get_donantes()

class SalidasForm(forms.Form):
    fecha_salida = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',  # HTML5 date+time picker
                'class': 'form-control',
            }
        ),
        required=True,
        initial=timezone.now,  # inicializa con la fecha/hora actual
    )

    al_entrada = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,  # o forms.SelectMultiple para un <select multiple>
        choices=[],  # se rellenará dinámicamente en __init__
        required=True,
    )

    beneficiario = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=[],  # se rellenará dinámicamente en __init__
        required=True,
    )

    num_tuppers = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        required=True,
        min_value=1
    )

    def __init__(self, *args, fecha_llegada=None, **kwargs):
        super().__init__(*args, **kwargs)
        if fecha_llegada is None:
            fecha_llegada = timezone.now() - timedelta(hours=12)
        self.fecha_salida_val = fecha_llegada  # guardamos para usar en get_al_entrada
        # Rellenar choices dinámicamente en cada instancia del formulario
        self.fields['al_entrada'].choices = get_alimentos_entrada(fecha_llegada=fecha_llegada)
        self.fields['beneficiario'].choices = get_beneficiarios()

