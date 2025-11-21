"""
Configuración de la aplicación proyectos
American Carpas 1 SAS
"""

from django.apps import AppConfig


class ProyectosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'proyectos'
    verbose_name = 'Gestión de Proyectos'
