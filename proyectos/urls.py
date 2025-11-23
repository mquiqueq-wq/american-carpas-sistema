"""
URLs para el módulo de gestión de proyectos
American Carpas 1 SAS
"""

from django.urls import path
from . import views

app_name = 'proyectos'

urlpatterns = [
    # Home del módulo
    path('', views.home_proyectos, name='home'),
    
    # =====================================================
    # FASE 1: CATÁLOGOS - TIPOS DE PROYECTOS
    # =====================================================
    path('catalogos/tipos/', views.tipo_proyecto_list, name='tipo_proyecto_list'),
    path('catalogos/tipos/crear/', views.tipo_proyecto_create, name='tipo_proyecto_create'),
    path('catalogos/tipos/<int:id_tipo_proyecto>/editar/', views.tipo_proyecto_update, name='tipo_proyecto_update'),
    path('catalogos/tipos/<int:id_tipo_proyecto>/eliminar/', views.tipo_proyecto_delete, name='tipo_proyecto_delete'),
    
    # =====================================================
    # FASE 1: CATÁLOGOS - ESTADOS DE PROYECTOS
    # =====================================================
    path('catalogos/estados/', views.estado_proyecto_list, name='estado_proyecto_list'),
    path('catalogos/estados/crear/', views.estado_proyecto_create, name='estado_proyecto_create'),
    path('catalogos/estados/<int:id_estado_proyecto>/editar/', views.estado_proyecto_update, name='estado_proyecto_update'),
    path('catalogos/estados/<int:id_estado_proyecto>/eliminar/', views.estado_proyecto_delete, name='estado_proyecto_delete'),
    
    # =====================================================
    # FASE 1: CATÁLOGOS - TIPOS DE DOCUMENTOS
    # =====================================================
    path('catalogos/documentos/', views.tipo_documento_list, name='tipo_documento_list'),
    path('catalogos/documentos/crear/', views.tipo_documento_create, name='tipo_documento_create'),
    path('catalogos/documentos/<int:id_tipo_documento>/editar/', views.tipo_documento_update, name='tipo_documento_update'),
    path('catalogos/documentos/<int:id_tipo_documento>/eliminar/', views.tipo_documento_delete, name='tipo_documento_delete'),
    
    # =====================================================
    # FASE 2: CLIENTES
    # =====================================================
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/crear/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:id_cliente>/', views.cliente_detail, name='cliente_detail'),
    path('clientes/<int:id_cliente>/editar/', views.cliente_update, name='cliente_update'),
    path('clientes/<int:id_cliente>/eliminar/', views.cliente_delete, name='cliente_delete'),
    
    # =====================================================
    # FASE 3: PROYECTOS
    # =====================================================
    path('listado/', views.proyecto_list, name='proyecto_list'),
    path('crear/', views.proyecto_create, name='proyecto_create'),
    path('<int:id_proyecto>/', views.proyecto_detail, name='proyecto_detail'),
    path('<int:id_proyecto>/editar/', views.proyecto_update, name='proyecto_update'),
    path('<int:id_proyecto>/eliminar/', views.proyecto_delete, name='proyecto_delete'),
    
    # =====================================================
    # FASE 4: ACTIVIDADES
    # =====================================================
    path('<int:id_proyecto>/actividades/', views.actividad_list, name='actividad_list'),
    path('<int:id_proyecto>/actividades/crear/', views.actividad_create, name='actividad_create'),
    path('actividades/<int:id_actividad>/editar/', views.actividad_update, name='actividad_update'),
    path('actividades/<int:id_actividad>/eliminar/', views.actividad_delete, name='actividad_delete'),
    
    # ====
    # FASE 4.1: AVANCES DE ACTIVIDADES
    # ====
    path('actividades/<int:id_actividad>/avances/', views.avance_list, name='avance_list'),
    path('actividades/<int:id_actividad>/avances/registrar/', views.avance_create, name='avance_create'),
    path('avances/<int:id_avance>/editar/', views.avance_update, name='avance_update'),
    path('avances/<int:id_avance>/eliminar/', views.avance_delete, name='avance_delete'),

    # GANTT
    
    #path('proyectos/<int:proyecto_id>/gantt-data/', views.proyecto_gantt_data, name='proyecto_gantt_data'),
    #path('proyectos/<int:proyecto_id>/gantt/', views.proyecto_gantt_view, name='proyecto_gantt_view'),
    #path('proyectos/<int:proyecto_id>/gantt-save/', views.proyecto_gantt_save, name='proyecto_gantt_save'),

    path('<int:proyecto_id>/gantt/', views.proyecto_gantt_view, name='proyecto_gantt_view'),
    path('<int:proyecto_id>/gantt-data/', views.proyecto_gantt_data, name='proyecto_gantt_data'),
    path('<int:proyecto_id>/gantt-save/', views.proyecto_gantt_save, name='proyecto_gantt_save'),
    path('<int:proyecto_id>/gantt/link/save/', views.proyecto_gantt_link_save, name='proyecto_gantt_link_save'),
    path('<int:proyecto_id>/gantt/link/delete/', views.proyecto_gantt_link_delete, name='proyecto_gantt_link_delete'),

    # Formulario de enlace (opcional, para edición manual)
    #path('proyecto/<int:proyecto_id>/enlace/crear/', views.proyecto_enlace_form, name='proyecto_enlace_crear'),
    #path('proyecto/<int:proyecto_id>/enlace/<int:enlace_id>/editar/', views.proyecto_enlace_form, name='proyecto_enlace_editar'),

    # =====================================================
    # FASE 5: ASIGNACIONES DE TRABAJADORES
    # =====================================================
    path('<int:id_proyecto>/trabajadores/', views.asignacion_list, name='asignacion_list'),
    path('<int:id_proyecto>/trabajadores/asignar/', views.asignacion_create, name='asignacion_create'),
    path('trabajadores/<int:id_asignacion>/editar/', views.asignacion_update, name='asignacion_update'),
    path('trabajadores/<int:id_asignacion>/eliminar/', views.asignacion_delete, name='asignacion_delete'),
    
    # =====================================================
    # FASE 6: DOCUMENTOS
    # =====================================================
    path('<int:id_proyecto>/documentos/', views.documento_list, name='documento_list'),
    path('<int:id_proyecto>/documentos/subir/', views.documento_create, name='documento_create'),
    path('documentos/<int:id_documento>/eliminar/', views.documento_delete, name='documento_delete'),
    
    # =====================================================
    # FASE 7: EVIDENCIAS FOTOGRÁFICAS
    # =====================================================
    path('<int:id_proyecto>/evidencias/', views.evidencia_list, name='evidencia_list'),
    path('<int:id_proyecto>/evidencias/subir/', views.evidencia_create, name='evidencia_create'),
    path('evidencias/<int:id_evidencia>/eliminar/', views.evidencia_delete, name='evidencia_delete'),
]
