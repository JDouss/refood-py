from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import Sum
from datetime import datetime, timedelta

from .forms import MenuPrincipalForm,EntradasForm,SalidasForm
from .models import AlEnt,Donante,TipoAl,AlSal,Benef

@login_required
def redirigir_por_grupo(request):
    if request.user.groups.filter(name='Administradores').exists():
        return redirect('/admin')
    else:
        return redirect('menu_principal')


@login_required
def menu_principal(request):
    return render(request, 'refood_app/menu_principal.html', {'form': MenuPrincipalForm()})


def entradas(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = EntradasForm(request.POST)
        if form.is_valid():
            # Obtener datos del formulario
            peso = form.cleaned_data['peso']
            fecha_llegada = form.cleaned_data['fecha_llegada']
            donante_id = form.cleaned_data['donante']
            tipo_al_id = form.cleaned_data['nombre_alimento']

            # Crear instancia del modelo
            AlEnt.objects.create(
                peso=peso,
                donante=Donante.objects.get(id=donante_id),
                tipo_al=TipoAl.objects.get(id=tipo_al_id),
                fecha_y_hora_entrada=fecha_llegada,
                fecha_y_hora_recogida=fecha_llegada,
                fecha_y_hora_preparacion=fecha_llegada,
            )

            return redirect('entradas')


    form = EntradasForm()
    print("DEBUG CHOICES:", list(form.fields['nombre_alimento'].choices))
    return render(request, 'refood_app/entradas.html', {
            'form': form,
        })

def salidas(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = SalidasForm(request.POST)
        if form.is_valid():
            fecha_salida = form.cleaned_data['fecha_salida']
            beneficiario_id = form.cleaned_data['beneficiario']
            al_entradas_ids = form.cleaned_data['al_entrada']

            beneficiario = Benef.objects.get(id=beneficiario_id)

            for al_ent_id in al_entradas_ids:
                al_ent = AlEnt.objects.get(id=al_ent_id)
                AlSal.objects.create(
                    fecha_salida=fecha_salida,
                    benef=beneficiario,
                    al_ent=al_ent
                )
            return redirect('salidas')

    form = SalidasForm()
    return render(request, 'refood_app/salidas.html', {
            'form': form,
        })

@login_required
def estadisticas(request):
    # Lógica para obtener los datos de los gráficos
    # Kilos totales por día (últimos 7 días)
    today = datetime.now().date()
    dates = [today - timedelta(days=i) for i in range(7)]
    dates.reverse() # Para tener las fechas en orden ascendente

    kilos_por_dia = []
    for d in dates:
        total_kilos = AlEnt.objects.filter(fecha_y_hora_entrada__date=d).aggregate(Sum('peso'))['peso__sum'] or 0
        kilos_por_dia.append(float(total_kilos)) # Convertir a float para Chart.js

    # Kilos medios por día (últimos 7 días)
    kilos_medios_por_dia = []
    for d in dates:
        total_kilos_salida = AlSal.objects.filter(fecha_salida__date=d).aggregate(Sum('al_ent__peso'))['al_ent__peso__sum'] or 0
        num_salidas = AlSal.objects.filter(fecha_salida__date=d).count()
        
        if num_salidas > 0:
            media_kilos = total_kilos_salida / num_salidas
        else:
            media_kilos = 0
        kilos_medios_por_dia.append(float(media_kilos))

    context = {
        'dates': [d.strftime('%Y-%m-%d') for d in dates],
        'kilos_por_dia': kilos_por_dia,
        'kilos_medios_por_dia': kilos_medios_por_dia,
    }
    return render(request, 'refood_app/estadisticas.html', context)
