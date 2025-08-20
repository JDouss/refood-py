from django.db import models
from django.utils import timezone

class TipoAl(models.Model):
    nombre_alimento = models.CharField(max_length=100)
    fruta_y_verdura = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre_alimento


class Donante(models.Model):
    id_donante = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    codigo_postal = models.CharField(max_length=10)
    provincia = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    responsable = models.CharField(max_length=100)
    fecha_alta = models.DateField()
    fecha_baja = models.DateField(null=True, blank=True)
    comentarios = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Benef(models.Model):
    id_beneficiario = models.CharField(max_length=10)
    nombre_representante = models.CharField(max_length=100)
    primer_apellido_representante = models.CharField(max_length=100)
    segundo_apellido_representante = models.CharField(max_length=100)
    numero_personas = models.IntegerField()
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    telefono_secundario = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    codigo_postal = models.CharField(max_length=10)
    fecha_alta = models.DateField()
    fecha_baja = models.DateField(null=True, blank=True)
    numero_ninios = models.IntegerField()
    activo = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_representante


class AlEnt(models.Model):
    peso = models.FloatField()
    fruta_y_verdura = models.BooleanField(default=False)
    fecha_y_hora_entrada = models.DateTimeField(default=timezone.now)
    fecha_y_hora_recogida = models.DateTimeField(null=True, blank=True)
    fecha_y_hora_preparacion = models.DateTimeField(default=timezone.now, null=True, blank=True)
    donante = models.ForeignKey(Donante, on_delete=models.CASCADE)
    tipo_al = models.ForeignKey(TipoAl, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo_al.nombre_alimento} - {self.fecha_y_hora_entrada}"


class AlSal(models.Model):
    fecha_salida = models.DateTimeField()
    benef = models.ForeignKey(Benef, on_delete=models.CASCADE)
    al_ent = models.ForeignKey(AlEnt, on_delete=models.CASCADE)

    def __str__(self):
        return f"Salida {self.id} - {self.fecha_salida}"

class Checkout(models.Model):
    fecha_salida = models.DateTimeField()
    peso = models.FloatField()
    benef = models.ForeignKey('Benef', on_delete=models.CASCADE)

    def __str__(self):
        return f"Checkout de {self.benef.nombre_representante} el {self.fecha_salida.strftime('%Y-%m-%d %H:%M')}"

