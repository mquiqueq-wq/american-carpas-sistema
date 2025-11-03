#!/bin/bash
set -e

echo "============================================"
echo "Iniciando aplicación Django..."
echo "============================================"

echo "Esperando a que MySQL esté disponible..."
sleep 5

echo "Probando conexión a la base de datos..."
python manage.py check --database default

echo "Ejecutando migraciones de Django..."
python manage.py migrate --noinput

echo "Verificando migraciones..."
python manage.py showmigrations

echo "Iniciando servidor Gunicorn..."
exec gunicorn american_carpas_project.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 4 --log-level info