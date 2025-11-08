#!/usr/bin/env python
"""
Script para crear superusuario usando variables de entorno
Configurar en Railway:
- DJANGO_SUPERUSER_USERNAME
- DJANGO_SUPERUSER_EMAIL  
- DJANGO_SUPERUSER_PASSWORD
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'american_carpas_1.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Leer desde variables de entorno
USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not PASSWORD:
    print('❌ Error: Debes configurar DJANGO_SUPERUSER_PASSWORD en Railway')
    exit(1)

# Verificar si ya existe
if User.objects.filter(username=USERNAME).exists():
    print(f'ℹ️ El usuario {USERNAME} ya existe')
else:
    # Crear superusuario
    User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    print(f'✅ Superusuario {USERNAME} creado exitosamente')
