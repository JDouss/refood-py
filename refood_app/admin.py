# refood_app/admin.py
from django.contrib import admin
from .models import Donante, TipoAl, AlEnt, Benef, AlSal, Checkout

admin.site.register(Donante)
admin.site.register(TipoAl)
admin.site.register(AlEnt)
admin.site.register(Benef)
admin.site.register(AlSal)
admin.site.register(Checkout)