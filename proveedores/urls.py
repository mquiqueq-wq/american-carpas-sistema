from django.urls import path
from . import views

app_name = "proveedores"

urlpatterns = [
    # ====================================
    # PÁGINA DE INICIO
    # ====================================
    path('', views.home_proveedores, name='home'),
    
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
    
    # ====================================
    # CRUD PROVEEDORES - FASE 2
    # ====================================
    path('listado/', views.proveedor_list, name='proveedor_list'),
    path('nuevo/', views.proveedor_create, name='proveedor_create'),
    path('<int:id_proveedor>/', views.proveedor_detail, name='proveedor_detail'),
    path('<int:id_proveedor>/editar/', views.proveedor_update, name='proveedor_update'),
    path('<int:id_proveedor>/eliminar/', views.proveedor_delete, name='proveedor_delete'),
    
    # ====================================
    # GESTIÓN DE CONTACTOS - FASE 3
    # ====================================
    path('<int:id_proveedor>/contacto/nuevo/', views.contacto_create, name='contacto_create'),
    path('contacto/<int:id_contacto>/editar/', views.contacto_update, name='contacto_update'),
    path('contacto/<int:id_contacto>/eliminar/', views.contacto_delete, name='contacto_delete'),
    
    # ====================================
    # GESTIÓN DE DOCUMENTOS - FASE 4
    # ====================================
    path('<int:id_proveedor>/documento/nuevo/', views.documento_create, name='documento_create'),
    path('documento/<int:id_documento>/editar/', views.documento_update, name='documento_update'),
    path('documento/<int:id_documento>/eliminar/', views.documento_delete, name='documento_delete'),
    path('documento/<int:id_documento>/descargar/', views.documento_download, name='documento_download'),
    
    # ====================================
    # GESTIÓN DE PRODUCTOS/SERVICIOS - FASE 5
    # ====================================
    path('<int:id_proveedor>/producto/nuevo/', views.producto_create, name='producto_create'),
    path('producto/<int:id_producto_servicio>/editar/', views.producto_update, name='producto_update'),
    path('producto/<int:id_producto_servicio>/eliminar/', views.producto_delete, name='producto_delete'),
]
