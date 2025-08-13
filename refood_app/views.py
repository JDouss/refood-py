from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import MenuPrincipalForm,EntradasForm,SalidasForm

@login_required
def redirigir_por_grupo(request):
    if request.user.groups.filter(name='Administradores').exists():
        return redirect('/admin')
    else:
        return redirect('menu_principal')


@login_required
def menu_principal(request):
    return render(request, 'refood_app/menu_principal.html', {'form': MenuPrincipalForm()})


def redirigir_formulario(request):
    tipo_form = request.GET.get('tipo_form')
    if tipo_form == 'entradas':
        return redirect('entradas')
    elif tipo_form == 'salidas':
        return redirect('salidas')
    else:
        return redirect('menu_principal')  # fallback si no hay tipo válido



def entradas(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EntradasForm(request.POST)
        # check whether it's valid:
        # process the data in form.cleaned_data as required
        # redirect to a new URL
        # Aqui copio a la DB los datos de localización


    form = EntradasForm()
    print("DEBUG CHOICES:", list(form.fields['nombre_alimento'].choices))
    return render(request, 'refood_app/entradas.html', {
            'form': form,
        })

def salidas(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SalidasForm(request.POST)
        # check whether it's valid:
        # process the data in form.cleaned_data as required
        # redirect to a new URL
        # Aqui copio a la DB los datos de localización
        form = SalidasForm()


    form = SalidasForm()
    return render(request, 'refood_app/salidas.html', {
            'form': form,
        })
