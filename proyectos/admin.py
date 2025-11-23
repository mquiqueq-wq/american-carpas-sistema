"""
Configuración del admin para el módulo de proyectos
American Carpas 1 SAS
"""

from django.contrib import admin
from .models import (
    TipoProyecto,
    EstadoProyecto,
    TipoDocumentoProyecto,
    Cliente,
    Proyecto,
    Actividad,
    AsignacionTrabajador,
    DocumentoProyecto,
    EvidenciaFotografica
)


@admin.register(TipoProyecto)
class TipoProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre_tipo', 'color_identificador', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre_tipo', 'descripcion']
    ordering = ['nombre_tipo']


@admin.register(EstadoProyecto)
class EstadoProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre_estado', 'color_badge', 'permite_edicion', 'es_estado_final', 'orden_visualizacion', 'activo']
    list_filter = ['activo', 'permite_edicion', 'es_estado_final']
    search_fields = ['nombre_estado', 'descripcion']
    ordering = ['orden_visualizacion', 'nombre_estado']


@admin.register(TipoDocumentoProyecto)
class TipoDocumentoProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre_tipo_documento', 'requiere_vigencia', 'dias_alerta_vencimiento', 'orden_visualizacion', 'activo']
    list_filter = ['activo', 'requiere_vigencia']
    search_fields = ['nombre_tipo_documento', 'descripcion']
    ordering = ['orden_visualizacion', 'nombre_tipo_documento']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['razon_social', 'numero_documento', 'tipo_documento', 'ciudad', 'telefono_principal', 'activo']
    list_filter = ['activo', 'tipo_documento', 'departamento']
    search_fields = ['razon_social', 'nombre_comercial', 'numero_documento', 'email_principal']
    ordering = ['razon_social']
    readonly_fields = ['fecha_registro']


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['codigo_proyecto', 'nombre_proyecto', 'cliente', 'tipo_proyecto', 'estado_proyecto', 'activo']
    list_filter = ['activo', 'estado_proyecto', 'tipo_proyecto', 'ciudad_proyecto']
    search_fields = ['codigo_proyecto', 'nombre_proyecto', 'cliente__razon_social', 'ingeniero_responsable']
    ordering = ['-fecha_registro']
    readonly_fields = ['fecha_registro', 'fecha_modificacion']
    date_hierarchy = 'fecha_registro'


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ['numero_actividad', 'nombre_actividad', 'proyecto', 'porcentaje_avance', 'activo']
    list_filter = ['activo', 'proyecto']
    search_fields = ['numero_actividad', 'nombre_actividad', 'proyecto__codigo_proyecto']
    ordering = ['proyecto', 'orden_visualizacion', 'numero_actividad']
    readonly_fields = ['fecha_registro']


@admin.register(AsignacionTrabajador)
class AsignacionTrabajadorAdmin(admin.ModelAdmin):
    list_display = ['trabajador', 'proyecto', 'rol_en_proyecto', 'fecha_asignacion', 'fecha_desasignacion', 'activo']
    list_filter = ['activo', 'proyecto', 'fecha_asignacion']
    search_fields = ['trabajador__nombres', 'trabajador__apellidos', 'proyecto__codigo_proyecto', 'rol_en_proyecto']
    ordering = ['-fecha_asignacion']
    readonly_fields = ['fecha_registro']
    date_hierarchy = 'fecha_asignacion'


@admin.register(DocumentoProyecto)
class DocumentoProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre_documento', 'proyecto', 'tipo_documento', 'fecha_emision', 'fecha_vencimiento', 'activo']
    list_filter = ['activo', 'tipo_documento', 'proyecto']
    search_fields = ['nombre_documento', 'numero_documento', 'proyecto__codigo_proyecto']
    ordering = ['-fecha_carga']
    readonly_fields = ['fecha_carga']
    date_hierarchy = 'fecha_carga'


@admin.register(EvidenciaFotografica)
class EvidenciaFotograficaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'proyecto', 'tipo_evidencia', 'fecha_captura', 'activo']
    list_filter = ['activo', 'tipo_evidencia', 'proyecto', 'fecha_captura']
    search_fields = ['titulo', 'descripcion', 'proyecto__codigo_proyecto']
    ordering = ['-fecha_captura', '-fecha_carga']
    readonly_fields = ['fecha_carga']
    date_hierarchy = 'fecha_captura'

from .models import EnlaceActividad

@admin.register(EnlaceActividad)
class EnlaceActividadAdmin(admin.ModelAdmin):
    list_display = ['actividad_origen', 'tipo_enlace', 'actividad_destino', 'lag', 'activo']
    list_filter = ['tipo_enlace', 'activo']
    search_fields = ['actividad_origen__nombre_actividad', 'actividad_destino__nombre_actividad']