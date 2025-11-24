"""
URLs para el módulo de Inventario de Carpas
American Carpas 1 SAS

Versión: 2.0 - Fase 2: Catálogos Básicos
"""

from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Home del módulo
    path('', views.home_inventario, name='home'),
    
    # =========================================================================
    # UBICACIONES DE ALMACÉN
    # =========================================================================
    path('ubicaciones/', views.UbicacionAlmacenListView.as_view(), name='ubicacion_list'),
    path('ubicaciones/nueva/', views.UbicacionAlmacenCreateView.as_view(), name='ubicacion_create'),
    path('ubicaciones/<int:pk>/editar/', views.UbicacionAlmacenUpdateView.as_view(), name='ubicacion_update'),
    path('ubicaciones/<int:pk>/eliminar/', views.UbicacionAlmacenDeleteView.as_view(), name='ubicacion_delete'),
    
    # =========================================================================
    # CATÁLOGOS DE LONAS
    # =========================================================================
    # Tipos de Lona
    path('catalogos/tipos-lona/', views.TipoLonaListView.as_view(), name='tipolona_list'),
    path('catalogos/tipos-lona/nuevo/', views.TipoLonaCreateView.as_view(), name='tipolona_create'),
    path('catalogos/tipos-lona/<int:pk>/editar/', views.TipoLonaUpdateView.as_view(), name='tipolona_update'),
    path('catalogos/tipos-lona/<int:pk>/eliminar/', views.TipoLonaDeleteView.as_view(), name='tipolona_delete'),
    
    # Anchos de Lona
    path('catalogos/anchos-lona/', views.AnchoLonaListView.as_view(), name='ancholona_list'),
    path('catalogos/anchos-lona/nuevo/', views.AnchoLonaCreateView.as_view(), name='ancholona_create'),
    path('catalogos/anchos-lona/<int:pk>/editar/', views.AnchoLonaUpdateView.as_view(), name='ancholona_update'),
    path('catalogos/anchos-lona/<int:pk>/eliminar/', views.AnchoLonaDeleteView.as_view(), name='ancholona_delete'),
    
    # Colores de Lona
    path('catalogos/colores-lona/', views.ColorLonaListView.as_view(), name='colorlona_list'),
    path('catalogos/colores-lona/nuevo/', views.ColorLonaCreateView.as_view(), name='colorlona_create'),
    path('catalogos/colores-lona/<int:pk>/editar/', views.ColorLonaUpdateView.as_view(), name='colorlona_update'),
    path('catalogos/colores-lona/<int:pk>/eliminar/', views.ColorLonaDeleteView.as_view(), name='colorlona_delete'),
    
    # Tratamientos de Lona
    path('catalogos/tratamientos-lona/', views.TratamientoLonaListView.as_view(), name='tratamientolona_list'),
    path('catalogos/tratamientos-lona/nuevo/', views.TratamientoLonaCreateView.as_view(), name='tratamientolona_create'),
    path('catalogos/tratamientos-lona/<int:pk>/editar/', views.TratamientoLonaUpdateView.as_view(), name='tratamientolona_update'),
    path('catalogos/tratamientos-lona/<int:pk>/eliminar/', views.TratamientoLonaDeleteView.as_view(), name='tratamientolona_delete'),
    
    # =========================================================================
    # CATÁLOGOS DE ESTRUCTURA
    # =========================================================================
    # Tipos de Estructura
    path('catalogos/tipos-estructura/', views.TipoEstructuraListView.as_view(), name='tipoestructura_list'),
    path('catalogos/tipos-estructura/nuevo/', views.TipoEstructuraCreateView.as_view(), name='tipoestructura_create'),
    path('catalogos/tipos-estructura/<int:pk>/editar/', views.TipoEstructuraUpdateView.as_view(), name='tipoestructura_update'),
    path('catalogos/tipos-estructura/<int:pk>/eliminar/', views.TipoEstructuraDeleteView.as_view(), name='tipoestructura_delete'),
    
    # Medidas de Tubo
    path('catalogos/medidas-tubo/', views.MedidaTuboListView.as_view(), name='medidatubo_list'),
    path('catalogos/medidas-tubo/nuevo/', views.MedidaTuboCreateView.as_view(), name='medidatubo_create'),
    path('catalogos/medidas-tubo/<int:pk>/editar/', views.MedidaTuboUpdateView.as_view(), name='medidatubo_update'),
    path('catalogos/medidas-tubo/<int:pk>/eliminar/', views.MedidaTuboDeleteView.as_view(), name='medidatubo_delete'),
    
    # Calibres
    path('catalogos/calibres/', views.CalibreListView.as_view(), name='calibre_list'),
    path('catalogos/calibres/nuevo/', views.CalibreCreateView.as_view(), name='calibre_create'),
    path('catalogos/calibres/<int:pk>/editar/', views.CalibreUpdateView.as_view(), name='calibre_update'),
    path('catalogos/calibres/<int:pk>/eliminar/', views.CalibreDeleteView.as_view(), name='calibre_delete'),
    
    # Materiales de Estructura
    path('catalogos/materiales/', views.MaterialEstructuraListView.as_view(), name='material_list'),
    path('catalogos/materiales/nuevo/', views.MaterialEstructuraCreateView.as_view(), name='material_create'),
    path('catalogos/materiales/<int:pk>/editar/', views.MaterialEstructuraUpdateView.as_view(), name='material_update'),
    path('catalogos/materiales/<int:pk>/eliminar/', views.MaterialEstructuraDeleteView.as_view(), name='material_delete'),
    
    # Acabados de Estructura
    path('catalogos/acabados/', views.AcabadoEstructuraListView.as_view(), name='acabado_list'),
    path('catalogos/acabados/nuevo/', views.AcabadoEstructuraCreateView.as_view(), name='acabado_create'),
    path('catalogos/acabados/<int:pk>/editar/', views.AcabadoEstructuraUpdateView.as_view(), name='acabado_update'),
    path('catalogos/acabados/<int:pk>/eliminar/', views.AcabadoEstructuraDeleteView.as_view(), name='acabado_delete'),
    
    # =========================================================================
    # CATÁLOGOS DE ACCESORIOS
    # =========================================================================
    path('catalogos/tipos-accesorio/', views.TipoAccesorioListView.as_view(), name='tipoaccesorio_list'),
    path('catalogos/tipos-accesorio/nuevo/', views.TipoAccesorioCreateView.as_view(), name='tipoaccesorio_create'),
    path('catalogos/tipos-accesorio/<int:pk>/editar/', views.TipoAccesorioUpdateView.as_view(), name='tipoaccesorio_update'),
    path('catalogos/tipos-accesorio/<int:pk>/eliminar/', views.TipoAccesorioDeleteView.as_view(), name='tipoaccesorio_delete'),
]