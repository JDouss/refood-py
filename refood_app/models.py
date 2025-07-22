# refood_app/models.py

from django.db import models
from django.utils import timezone

# Donante model is correct
class Donante(models.Model):
    id_donante = models.CharField(max_length=20, unique=True, verbose_name="Donor ID")
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id_donante} - {self.nombre}"

# TipoAl model is correct
class TipoAl(models.Model):
    nombre_alimento = models.CharField(max_length=100)
    fruta_y_verdura = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_alimento

# AlEnt model is correct
class AlEnt(models.Model):
    peso = models.FloatField()
    donante = models.ForeignKey(Donante, on_delete=models.CASCADE)
    tipo_al = models.ForeignKey(TipoAl, on_delete=models.CASCADE)
    fecha_y_hora_entrada = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.tipo_al.nombre_alimento} from {self.donante.nombre} at {self.fecha_y_hora_entrada.strftime('%Y-%m-%d %H:%M')}"

# Benef model is correct
class Benef(models.Model):
    id_beneficiario = models.CharField(max_length=20, unique=True, verbose_name="Beneficiary ID")
    nombre_representante = models.CharField(max_length=100)
    numero_personas = models.IntegerField()
    telefono = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id_beneficiario} - {self.nombre_representante}"

# --- NEW AND REVISED MODELS BELOW ---

# NEW 'Checkout' model
# This represents the final, weighed package for a single beneficiary.
class Checkout(models.Model):
    beneficiario = models.ForeignKey(Benef, on_delete=models.CASCADE)
    peso = models.FloatField() # The total weight of the final package
    fecha_salida = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Package for {self.beneficiario.nombre_representante} on {self.fecha_salida.strftime('%Y-%m-%d')}"

# REVISED 'AlSal' (Outgoing Food) model
# This now represents an individual, unweighed portion that BELONGS to a Checkout package.
class AlSal(models.Model):
    alimento_entrada = models.ForeignKey(AlEnt, on_delete=models.CASCADE, related_name="porciones_salida")
    # The link to the beneficiary is now through the Checkout model.
    # A portion is part of a checkout package. This is nullable initially.
    checkout = models.ForeignKey(Checkout, on_delete=models.SET_NULL, null=True, blank=True, related_name="porciones")

    def __str__(self):
        return f"Portion of {self.alimento_entrada.tipo_al.nombre_alimento}"