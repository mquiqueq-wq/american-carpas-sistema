from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "trabajadores"

urlpatterns = [
    # ====================================
    # PÁGINA DE INICIO (home con iconos)
    # ====================================
    path('', TemplateView.as_view(
        template_name='trabajadores/home_trabajadores.html',
        extra_context={'show_module_nav': True, 'active_module': 'trabajadores'}
    ), name='home'),
    
    # ====================================
    # LISTADO Y CRUD BÁSICO
    # ====================================
    path('listado/', views.trabajador_list, name='trabajador_list'),
    path('nuevo/', views.trabajador_create, name='trabajador_create'),
    
    # ====================================
    # GESTIÓN DE CATÁLOGOS (ANTES de rutas dinámicas)
    # ====================================
    # Tipos de Cursos
    path('catalogos/tipos-cursos/', views.tipo_curso_list, name='tipo_curso_list'),
    path('catalogos/tipos-cursos/nuevo/', views.tipo_curso_create, name='tipo_curso_create'),
    path('catalogos/tipos-cursos/<int:id_tipo_curso>/editar/', views.tipo_curso_update, name='tipo_curso_update'),
    path('catalogos/tipos-cursos/<int:id_tipo_curso>/eliminar/', views.tipo_curso_delete, name='tipo_curso_delete'),
    
    # Tipos de Dotaciones
    path('catalogos/tipos-dotaciones/', views.tipo_dotacion_list, name='tipo_dotacion_list'),
    path('catalogos/tipos-dotaciones/nuevo/', views.tipo_dotacion_create, name='tipo_dotacion_create'),
    path('catalogos/tipos-dotaciones/<int:id_tipo_dotacion>/editar/', views.tipo_dotacion_update, name='tipo_dotacion_update'),
    path('catalogos/tipos-dotaciones/<int:id_tipo_dotacion>/eliminar/', views.tipo_dotacion_delete, name='tipo_dotacion_delete'),
    
     # Tipos de Documentos
    path('catalogos/tipos-documentos/', views.tipo_documento_list, name='tipo_documento_list'),
    path('catalogos/tipos-documentos/nuevo/', views.tipo_documento_create, name='tipo_documento_create'),
    path('catalogos/tipos-documentos/<int:id_tipo_documento>/editar/', views.tipo_documento_update, name='tipo_documento_update'),
    path('catalogos/tipos-documentos/<int:id_tipo_documento>/eliminar/', views.tipo_documento_delete, name='tipo_documento_delete'),

    # ====================================
    # DASHBOARDS (ANTES de rutas dinámicas)
    # ====================================
    path('dashboard/', views.dashboard_general, name='dashboard_general'),
    path('dashboard/alertas-cursos/', views.dashboard_alertas_cursos, name='dashboard_alertas_cursos'),
    path('dashboard/alertas-dotaciones/', views.dashboard_alertas_dotaciones, name='dashboard_alertas_dotaciones'),

    # ====================================
    # LISTADOS Y REPORTES DE DOCUMENTOS
    # ====================================
    path('documentos/', views.documentos_list, name='documentos_list'),
    path('documentos/alertas/', views.documentos_vencidos, name='documentos_vencidos'),
    path('documentos/faltantes/', views.documentos_faltantes, name='documentos_faltantes'),
    
    # ====================================
    # REPORTES (ANTES de rutas dinámicas)
    # ====================================
    path('reporte/documentacion-incompleta/', views.reporte_trabajadores_sin_documentacion, name='reporte_documentacion_incompleta'),
    
    # ====================================
    # EXPORTACIONES (ANTES de rutas dinámicas)
    # ====================================
    path('exportar/custom/excel/', views.export_trabajadores_excel_custom, name='export_trabajadores_excel_custom'),
    path('exportar/custom/pdf/', views.export_trabajadores_pdf_custom, name='export_trabajadores_pdf_custom'),

    # Exportación de documentos múltiples
    path('documentos/exportar/zip/', views.export_documentos_multiple_zip, name='export_documentos_multiple_zip'),
    
    # ====================================
    # URLs con parámetros dinámicos (AL FINAL)
    # ====================================
    
    # CRUD: TrabajadorPersonal (detalle, editar, eliminar)
    path('<str:id_trabajador>/', views.trabajador_detail, name='trabajador_detail'),
    path('<str:id_trabajador>/editar/', views.trabajador_update, name='trabajador_update'),
    path('<str:id_trabajador>/eliminar/', views.trabajador_delete, name='trabajador_delete'),
    
    # Exportar PDF individual
    path('<str:id_trabajador>/exportar/pdf/', views.export_trabajador_pdf, name='export_trabajador_pdf'),

    # ====================================
    # CRUD: Registros laborales
    # ====================================
    path('<str:id_trabajador>/laboral/nuevo/', views.laboral_create, name='laboral_create'),
    path('laboral/<int:id_laboral>/editar/', views.laboral_update, name='laboral_update'),
    path('laboral/<int:id_laboral>/eliminar/', views.laboral_delete, name='laboral_delete'),

    # ====================================
    # CRUD: Afiliaciones
    # ====================================
    path('<str:id_trabajador>/afiliacion/nuevo/', views.afiliacion_create, name='afiliacion_create'),
    path('afiliacion/<int:id_afiliacion>/editar/', views.afiliacion_update, name='afiliacion_update'),
    path('afiliacion/<int:id_afiliacion>/eliminar/', views.afiliacion_delete, name='afiliacion_delete'),

    # ====================================
    # CRUD: Dotación
    # ====================================
    path('<str:id_trabajador>/dotacion/nuevo/', views.dotacion_create, name='dotacion_create'),
    path('dotacion/<int:id_dotacion>/editar/', views.dotacion_update, name='dotacion_update'),
    path('dotacion/<int:id_dotacion>/eliminar/', views.dotacion_delete, name='dotacion_delete'),

    # ====================================
    # CRUD: Cursos
    # ====================================
    path('<str:id_trabajador>/curso/nuevo/', views.curso_create, name='curso_create'),
    path('curso/<int:id_curso>/editar/', views.curso_update, name='curso_update'),
    path('curso/<int:id_curso>/eliminar/', views.curso_delete, name='curso_delete'),

    # ====================================
    # CRUD: Documentos
    # ====================================
    path('<str:id_trabajador>/documento/nuevo/', views.documento_create, name='documento_create'),
    path('<str:id_trabajador>/documentos/exportar/zip/', views.export_documentos_trabajador_zip, name='export_documentos_trabajador_zip'),
    path('documento/<int:id_documento>/editar/', views.documento_update, name='documento_update'),
    path('documento/<int:id_documento>/eliminar/', views.documento_delete, name='documento_delete'),
    path('documento/<int:id_documento>/descargar/', views.documento_download, name='documento_download'),

    # ====================================
    # CRUD: Roles
    # ====================================
    path('<str:id_trabajador>/rol/nuevo/', views.rol_create, name='rol_create'),
    path('rol/<int:id_rol_sistema>/editar/', views.rol_update, name='rol_update'),
    path('rol/<int:id_rol_sistema>/eliminar/', views.rol_delete, name='rol_delete'),
]