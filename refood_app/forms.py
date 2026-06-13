from datetime import datetime,timedelta, date
from email.policy import default

from django import forms
from django.db import connections
from django.utils import timezone
from .models import AlEnt,TipoAl,Donante,Benef, AlSal # Importar AlSal

def get_tipos_alimentos():
    return TipoAl.objects.values_list('id', 'nombre_alimento').order_by('nombre_alimento')

def get_donantes():
    return Donante.objects.values_list('id','nombre')

def get_beneficiarios():
    beneficiarios = Benef.objects.filter(activo=1).values_list("id", "id_beneficiario", "nombre_representante").order_by('id_beneficiario')
    return [
        (b[0], f"{b[1]} - {b[2]}")
        for b in beneficiarios
    ]

def get_alimentos_entrada(min_date: date): # Cambiado selected_date a min_date
    # Obtener IDs de AlEnt que ya han sido usados en AlSal
    used_al_ent_ids = AlSal.objects.values_list('al_ent_id', flat=True)

    # Filtrar AlEnt que no están usados y cuya fecha de entrada es igual o posterior a la min_date
    al_entrada = (AlEnt.objects.exclude(id__in=used_al_ent_ids)
                  .filter(fecha_y_hora_entrada__date__gte=min_date) # Cambiado de lte a gte
                  .select_related("donante", "tipo_al")
                  .values_list("id", "tipo_al__nombre_alimento", "donante__nombre", "fecha_y_hora_entrada"))
    
    # Formatear para mostrar, incluyendo la fecha y manteniendo el orden alfabético
    # Primero ordenar por nombre de alimento, luego por fecha de entrada
    sorted_al_entrada = sorted(al_entrada, key=lambda x: (x[1], x[3]))

    return [
        (a[0], f"{a[1]} - {a[2]} ({a[3].strftime('%Y-%m-%d')})")
        for a in sorted_al_entrada
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
        # Ordenar alfabeticamente
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

    def __init__(self, *args, min_date=None, **kwargs): # Cambiado selected_date a min_date
        super().__init__(*args, **kwargs)
        if min_date is None:
            min_date = timezone.localdate() # Por defecto, la fecha actual
        
        self.fields['al_entrada'].choices = get_alimentos_entrada(min_date=min_date) # Pasar min_date
        self.fields['beneficiario'].choices = get_beneficiarios()