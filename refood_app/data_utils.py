import json
from datetime import datetime, timedelta, date
from django.db.models import Sum, Min, Count
from django.db.models.functions import TruncDate, ExtractWeekDay

from .models import AlEnt, Donante, Benef # Importar el modelo Benef

def get_all_entries_data_for_frontend():
    """
    Obtiene todos los datos de AlEnt necesarios para los gráficos y los devuelve
    en un formato que puede ser fácilmente procesado por JavaScript en el frontend.
    """
    all_entries = AlEnt.objects.select_related('donante').values(
        'fecha_y_hora_entrada', 'peso', 'donante__nombre'
    ).order_by('fecha_y_hora_entrada')

    processed_data = []
    for entry in all_entries:
        processed_data.append({
            'date': entry['fecha_y_hora_entrada'].strftime('%Y-%m-%d'),
            'weekday': entry['fecha_y_hora_entrada'].isoweekday(), # 1=Lunes, 7=Domingo
            'peso': float(entry['peso']),
            'donante_nombre': entry['donante__nombre']
        })
    return processed_data

def get_overall_statistics_data():
    """
    Calcula las estadísticas generales de todas las entradas.
    """
    total_kilos = AlEnt.objects.aggregate(Sum('peso'))['peso__sum'] or 0
    
    min_date_entry = AlEnt.objects.aggregate(Min('fecha_y_hora_entrada'))['fecha_y_hora_entrada__min']
    min_date = min_date_entry.strftime('%Y-%m-%d') if min_date_entry else 'N/A'

    distinct_dates_count = AlEnt.objects.annotate(
        entry_date=TruncDate('fecha_y_hora_entrada')
    ).values('entry_date').distinct().count()

    avg_kilos_per_day = (total_kilos / distinct_dates_count) if distinct_dates_count > 0 else 0

    # Nuevas estadísticas
    # Sumar el campo 'numero_personas' para el total de beneficiarios
    total_beneficiarios = Benef.objects.aggregate(Sum('numero_personas'))['numero_personas__sum'] or 0
    # Sumar el campo 'numero_personas' para los beneficiarios activos
    beneficiarios_activos = Benef.objects.filter(activo=True).aggregate(Sum('numero_personas'))['numero_personas__sum'] or 0
    total_donantes = Donante.objects.count()


    return {
        'total_kilos': float(total_kilos),
        'min_date': min_date,
        'total_days_worked': distinct_dates_count,
        'avg_kilos_per_day': float(f"{avg_kilos_per_day:.2f}"),
        'total_beneficiarios': total_beneficiarios,
        'beneficiarios_activos': beneficiarios_activos,
        'total_donantes': total_donantes,
    }