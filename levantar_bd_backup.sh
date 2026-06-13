#!/bin/bash

# 1. Verificar que se ha pasado el archivo como argumento
if [ -z "$1" ]; then
    echo "Error: Debes indicar la ruta al archivo .sql"
    echo "Uso: $0 /ruta/al/archivo.sql"
    exit 1
fi

SQL_FILE="$1"

# 2. Verificar que el archivo realmente existe
if [ ! -f "$SQL_FILE" ]; then
    echo "Error: El archivo '$SQL_FILE' no existe."
    exit 1
fi

# =====================================================================
# CONFIGURACIÓN (Sin contraseñas guardadas)
# =====================================================================
DB_USER="root"
DB_HOST="localhost"

# Datos del nuevo usuario para Django
NEW_USER="django_user"
NEW_USER_PASS="tu_password" # Esta sí la dejo aquí para que se configure sola, pero puedes cambiarla
# =====================================================================

echo "🔍 Analizando el archivo para encontrar el nombre de la base de datos..."

# 3. Extraer el nombre de la BD del archivo dump
DB_NAME=$(grep -o -E 'CREATE DATABASE /\*\!32312 IF NOT EXISTS\*/ `[^`]+`|CREATE DATABASE `[^`]+`|USE `[^`]+`' "$SQL_FILE" | head -n 1 | grep -o -E '`[^`]+`' | tr -d '`')

if [ -z "$DB_NAME" ]; then
    DB_NAME="refood_app_db"
fi

echo "📦 Base de datos detectada: $DB_NAME"
echo "----------------------------------------------"
echo "🔐 Se te solicitará la contraseña de MySQL ('$DB_USER') varias veces para confirmar las operaciones."
echo "----------------------------------------------"

# 4. Borrar base de datos si existe (-p forzará a pedirte la clave en la terminal)
echo "🗑️  Eliminando la base de datos '$DB_NAME' (si existe)..."
mysql -h "$DB_HOST" -u "$DB_USER" -p -e "DROP DATABASE IF EXISTS \`$DB_NAME\`;"

# 5. Crear la base de datos limpia
echo "🏗️  Creando la base de datos '$DB_NAME' limpia..."
mysql -h "$DB_HOST" -u "$DB_USER" -p -e "CREATE DATABASE \`$DB_NAME\`;"

# 6. Crear el usuario y asignar privilegios
echo "👤 Configurando el usuario '$NEW_USER'..."
mysql -h "$DB_HOST" -u "$DB_USER" -p -e "
    DROP USER IF EXISTS '$NEW_USER'@'localhost';
    CREATE USER '$NEW_USER'@'localhost' IDENTIFIED BY '$NEW_USER_PASS';
    GRANT ALL PRIVILEGES ON \`$DB_NAME\`.* TO '$NEW_USER'@'localhost';
    FLUSH PRIVILEGES;
"

# 7. Importar el esquema y contenido
echo "🚀 Importando el esquema y contenido desde '$SQL_FILE'..."
mysql -h "$DB_HOST" -u "$DB_USER" -p "$DB_NAME" < "$SQL_FILE"

if [ $? -eq 0 ]; then
    echo "----------------------------------------------"
    echo "✅ ¡Proceso completado con éxito!"
    echo "🌐 BD local limpia: $DB_NAME"
    echo "🔑 Usuario Django configurado."
else
    echo "❌ Hubo un error durante la importación del archivo SQL."
fi
