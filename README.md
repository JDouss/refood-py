# Refood App

Refood App es una aplicación web desarrollada con Django para la gestión de alimentos, entradas y salidas de beneficiarios, con soporte para usuarios administradores y usuarios normales.

---

## 1. Instalación

Sigue estos pasos para instalar y poner en marcha la aplicación en tu entorno local:

### a) Crear entorno virtual
```bash
python3 -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows

b) Instalar dependencias

pip install --upgrade pip
pip install -r requirements.txt

c) Instalar y configurar MySQL

    Instala MySQL según tu sistema operativo.

    Accede a MySQL y crea el usuario y base de datos:

CREATE DATABASE refood_app_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'tu_password';
GRANT ALL PRIVILEGES ON refood_app_db.* TO 'django_user'@'localhost';
FLUSH PRIVILEGES;

    Configura settings.py para usar la base de datos:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'refood_app_db',
        'USER': 'django_user',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

d) Aplicar migraciones

python manage.py makemigrations
python manage.py migrate

e) Crear superusuario (administrador)

python manage.py createsuperuser

f) Ejecutar el servidor

python manage.py runserver

Ahora podrás acceder a la aplicación en http://127.0.0.1:8000/.
2. Explicación de usuarios

La aplicación cuenta con dos tipos de usuarios:

    Administradores: pueden acceder al panel de administración y gestionar datos.

    Usuarios normales: tienen acceso limitado a ciertas funcionalidades (formularios de entrada y salida).

    Nota: En la primera puesta en marcha, para poder acceder al administrador, es posible desactivar temporalmente la función de login comentando la URL o el decorador @login_required. Por ejemplo:

# urls.py
# path('accounts/login/', LoginView.as_view(), name='login'),  # Comentar temporalmente

O en la vista que requiera login:

# views.py
# @login_required  # Comentar para poder acceder sin autenticación

Recuerda restaurar estas líneas después de crear el superusuario.
3. Formularios de Entrada y Salida
a) Formulario de Entradas (EntradasForm)

Campos:

    nombre_alimento (ChoiceField): selecciona el tipo de alimento.

    peso (DecimalField): peso del alimento en kg.

    donante (ChoiceField): selecciona el donante del alimento.

    fecha_llegada (DateTimeField): fecha y hora de entrada, inicializada con la fecha actual.

Modelo asociado: AlEnt
b) Formulario de Salidas (SalidasForm)

Campos:

    fecha_salida (DateTimeField): fecha y hora de salida, inicializada con la fecha actual.

    al_entrada (MultipleChoiceField): lista de alimentos de entrada disponibles para seleccionar.

    beneficiario (ChoiceField): selecciona el beneficiario.

    num_tuppers (IntegerField): cantidad de tuppers entregados.

Modelo asociado: AlSal

Por cada alimento seleccionado en al_entrada, se crea un registro independiente en AlSal. Las fechas se almacenan con hora y minuto gracias al campo DateTimeField.
