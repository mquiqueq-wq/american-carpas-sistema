"""
URL configuration for american_carpas_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    # Home general
    path('', TemplateView.as_view(template_name='home_general.html'), name='home_general'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # App trabajadores
    path('trabajadores/', include('trabajadores.urls')),

    # App proveedores
    path('proveedores/', include('proveedores.urls')),

    # App proyectos
    path('proyectos/', include('proyectos.urls')),

    # App inventario
    path('inventario/', include('inventario.urls')),

    # Página de próximamente
    path('proximamente/', TemplateView.as_view(template_name='proximamente.html'), name='proximamente'),
    
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)