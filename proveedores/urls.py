from django.urls import path
from . import views

app_name = "proveedores"

urlpatterns = [
    # ====================================
    # PÁGINA DE INICIO
    # ====================================
    path('', views.home, name='home'),
    
    # ====================================
    # GESTIÓN DE CATÁLOGOS
    # ====================================
    
    # Tipos de Proveedores
    path('catalogos/tipos-proveedores/', views.tipo_proveedor_list, name='tipo_proveedor_list'),
    path('catalogos/tipos-proveedores/nuevo/', views.tipo_proveedor_create, name='tipo_proveedor_create'),
    path('catalogos/tipos-proveedores/<int:id_tipo_proveedor>/editar/', views.tipo_proveedor_update, name='tipo_proveedor_update'),
    path('catalogos/tipos-proveedores/<int:id_tipo_proveedor>/eliminar/', views.tipo_proveedor_delete, name='tipo_proveedor_delete'),
    
    # Categorías de Proveedores
    path('catalogos/categorias/', views.categoria_proveedor_list, name='categoria_proveedor_list'),
    path('catalogos/categorias/nuevo/', views.categoria_proveedor_create, name='categoria_proveedor_create'),
    path('catalogos/categorias/<int:id_categoria>/editar/', views.categoria_proveedor_update, name='categoria_proveedor_update'),
    path('catalogos/categorias/<int:id_categoria>/eliminar/', views.categoria_proveedor_delete, name='categoria_proveedor_delete'),
    
    # Tipos de Documentos
    path('catalogos/tipos-documentos/', views.tipo_documento_list, name='tipo_documento_list'),
    path('catalogos/tipos-documentos/nuevo/', views.tipo_documento_create, name='tipo_documento_create'),
    path('catalogos/tipos-documentos/<int:id_tipo_documento>/editar/', views.tipo_documento_update, name='tipo_documento_update'),
    path('catalogos/tipos-documentos/<int:id_tipo_documento>/eliminar/', views.tipo_documento_delete, name='tipo_documento_delete'),
]
