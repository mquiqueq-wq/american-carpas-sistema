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


# =====================================================
# ADMIN PARA PROVEEDORES - FASE 2
# =====================================================

from .models import Proveedor

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = [
        'razon_social',
        'numero_documento',
        'tipo_proveedor',
        'categoria_principal',
        'ciudad',
        'telefono_principal',
        'estado',
        'fecha_registro'
    ]
    list_filter = ['estado', 'tipo_proveedor', 'categoria_principal', 'regimen_tributario']
    search_fields = [
        'razon_social',
        'nombre_comercial',
        'numero_documento',
        'ciudad',
        'email_principal'
    ]
    ordering = ['razon_social']
    date_hierarchy = 'fecha_registro'
    
    fieldsets = (
        ('Identificación Básica', {
            'fields': (
                'razon_social',
                'nombre_comercial',
                'tipo_documento',
                ('numero_documento', 'digito_verificacion'),
                'tipo_proveedor',
                'categoria_principal',
                'estado'
            )
        }),
        ('Información Legal y Tributaria', {
            'fields': (
                'regimen_tributario',
                'responsabilidad_fiscal',
                'actividad_economica',
                'codigo_ciiu',
                'pais_origen'
            ),
            'classes': ('collapse',)
        }),
        ('Información de Contacto', {
            'fields': (
                'direccion_principal',
                ('ciudad', 'departamento'),
                ('pais', 'codigo_postal'),
                ('telefono_principal', 'telefono_secundario'),
                ('email_principal', 'email_facturacion'),
                'sitio_web',
                'horario_atencion'
            )
        }),
        ('Información Bancaria', {
            'fields': (
                'banco',
                'tipo_cuenta',
                'numero_cuenta',
                'titular_cuenta'
            ),
            'classes': ('collapse',)
        }),
        ('Condiciones Comerciales', {
            'fields': (
                'plazo_entrega_dias',
                'tiempo_credito_dias',
                'descuento_pronto_pago',
                'monto_minimo_pedido',
                'acepta_credito',
                'metodos_pago_aceptados'
            ),
            'classes': ('collapse',)
        }),
        ('Control y Seguimiento', {
            'fields': (
                'fecha_ultima_compra',
                'total_compras_historico',
                'calificacion_promedio',
                'numero_evaluaciones',
                'registrado_por',
                'observaciones_generales'
            ),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_registro', 'fecha_ultima_modificacion']


# =====================================================
# ADMIN PARA CONTACTOS - FASE 3
# =====================================================

from .models import ContactoProveedor

@admin.register(ContactoProveedor)
class ContactoProveedorAdmin(admin.ModelAdmin):
    list_display = [
        'nombre_completo',
        'cargo',
        'id_proveedor',
        'area_responsabilidad',
        'telefono_celular',
        'email',
        'es_contacto_principal',
        'activo'
    ]
    list_filter = ['area_responsabilidad', 'es_contacto_principal', 'activo']
    search_fields = [
        'nombre_completo',
        'cargo',
        'email',
        'id_proveedor__razon_social'
    ]
    ordering = ['id_proveedor', '-es_contacto_principal', 'nombre_completo']
    
    fieldsets = (
        ('Proveedor', {
            'fields': ('id_proveedor',)
        }),
        ('Información del Contacto', {
            'fields': (
                'nombre_completo',
                'cargo',
                'departamento',
                'area_responsabilidad'
            )
        }),
        ('Datos de Contacto', {
            'fields': (
                'telefono_celular',
                'telefono_directo',
                'email'
            )
        }),
        ('Configuración', {
            'fields': (
                'es_contacto_principal',
                'activo',
                'observaciones'
            )
        }),
    )
    
    readonly_fields = ['fecha_registro', 'fecha_modificacion']
