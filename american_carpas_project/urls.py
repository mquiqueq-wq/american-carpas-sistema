"""
URL configuration for american_carpas_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    # Ruta raíz - redirige a trabajadores
    path('', lambda request: redirect('trabajadores/')),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # App trabajadores
    path('trabajadores/', include('trabajadores.urls')),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)