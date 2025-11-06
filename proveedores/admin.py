from django.contrib import admin
from .models import TipoProveedor, CategoriaProveedor, TipoDocumentoProveedor


# =====================================================
# ADMIN PARA TIPOS DE PROVEEDORES
# =====================================================

@admin.register(TipoProveedor)
class TipoProveedorAdmin(admin.ModelAdmin):
    list_display = [
        'nombre_tipo',
        'requiere_certificaciones',
        'activo',
        'orden_visualizacion',
        'fecha_creacion'
    ]
    list_filter = ['activo', 'requiere_certificaciones']
    search_fields = ['nombre_tipo', 'descripcion']
    ordering = ['orden_visualizacion', 'nombre_tipo']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre_tipo', 'descripcion', 'icono_bootstrap')
        }),
        ('Configuración', {
            'fields': ('requiere_certificaciones', 'activo', 'orden_visualizacion')
        }),
    )


# =====================================================
# ADMIN PARA CATEGORÍAS DE PROVEEDORES
# =====================================================

@admin.register(CategoriaProveedor)
class CategoriaProveedorAdmin(admin.ModelAdmin):
    list_display = [
        'nombre_categoria',
        'categoria_padre',
        'color_badge',
        'activo',
        'orden_visualizacion',
        'fecha_creacion'
    ]
    list_filter = ['activo', 'color_badge', 'categoria_padre']
    search_fields = ['nombre_categoria', 'descripcion']
    ordering = ['orden_visualizacion', 'nombre_categoria']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre_categoria', 'descripcion', 'categoria_padre')
        }),
        ('Visualización', {
            'fields': ('color_badge', 'icono_bootstrap', 'orden_visualizacion')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )


# =====================================================
# ADMIN PARA TIPOS DE DOCUMENTOS
# =====================================================

@admin.register(TipoDocumentoProveedor)
class TipoDocumentoProveedorAdmin(admin.ModelAdmin):
    list_display = [
        'nombre_tipo_documento',
        'es_obligatorio',
        'requiere_vigencia',
        'dias_alerta_vencimiento',
        'activo',
        'orden_visualizacion'
    ]
    list_filter = ['activo', 'es_obligatorio', 'requiere_vigencia']
    search_fields = ['nombre_tipo_documento', 'descripcion']
    ordering = ['orden_visualizacion', 'nombre_tipo_documento']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre_tipo_documento', 'descripcion', 'icono_bootstrap')
        }),
        ('Configuración', {
            'fields': (
                'es_obligatorio',
                'requiere_vigencia',
                'dias_alerta_vencimiento',
            )
        }),
        ('Visualización', {
            'fields': ('activo', 'orden_visualizacion')
        }),
    )
