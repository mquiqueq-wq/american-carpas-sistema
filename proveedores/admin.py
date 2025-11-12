"""
Configuración del Admin para el módulo de gestión de proveedores
American Carpas 1 SAS
"""

from django.contrib import admin
from .models import (
    TipoProveedor,
    CategoriaProveedor,
    TipoDocumentoProveedor,
    Proveedor,
    ContactoProveedor,
    DocumentoProveedor,
    ProductoServicioProveedor
)


# =====================================================
# ADMIN PARA CATÁLOGOS - FASE 1
# =====================================================

@admin.register(TipoProveedor)
class TipoProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre_tipo', 'activo', 'fecha_creacion']
    list_filter = ['activo']
    search_fields = ['nombre_tipo', 'descripcion']
    ordering = ['nombre_tipo']
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre_tipo', 'descripcion', 'icono')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )
    
    readonly_fields = ['fecha_creacion']


@admin.register(CategoriaProveedor)
class CategoriaProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre_categoria', 'categoria_padre', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'categoria_padre']
    search_fields = ['nombre_categoria', 'descripcion']
    ordering = ['nombre_categoria']
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre_categoria', 'descripcion', 'categoria_padre')
        }),
        ('Visualización', {
            'fields': ('icono', 'color')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )
    
    readonly_fields = ['fecha_creacion']


@admin.register(TipoDocumentoProveedor)
class TipoDocumentoProveedorAdmin(admin.ModelAdmin):
    list_display = [
        'nombre_tipo_documento',
        'obligatorio',
        'requiere_vigencia',
        'dias_alerta_vencimiento',
        'activo',
        'fecha_creacion'
    ]
    list_filter = ['obligatorio', 'requiere_vigencia', 'activo']
    search_fields = ['nombre_tipo_documento', 'descripcion']
    ordering = ['nombre_tipo_documento']
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre_tipo_documento', 'descripcion', 'icono')
        }),
        ('Configuración', {
            'fields': ('obligatorio', 'requiere_vigencia', 'dias_alerta_vencimiento')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )
    
    readonly_fields = ['fecha_creacion']


# =====================================================
# ADMIN PARA PROVEEDOR - FASE 2
# =====================================================

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = [
        'razon_social',
        'numero_documento',
        'tipo_proveedor',
        'categoria_principal',
        'ciudad',
        'estado',
        'fecha_registro'
    ]
    list_filter = ['estado', 'tipo_proveedor', 'categoria_principal', 'tipo_persona']
    search_fields = ['razon_social', 'nombre_comercial', 'numero_documento', 'email_principal']
    ordering = ['razon_social']
    date_hierarchy = 'fecha_registro'
    
    fieldsets = (
        ('Identificación Básica', {
            'fields': (
                'tipo_persona',
                'razon_social',
                'nombre_comercial',
                'tipo_documento',
                'numero_documento',
                'digito_verificacion'
            )
        }),
        ('Clasificación', {
            'fields': ('tipo_proveedor', 'categoria_principal')
        }),
        ('Información Legal y Tributaria', {
            'fields': (
                'regimen_tributario',
                'responsabilidad_fiscal',
                'pais_origen',
                'actividad_economica',
                'codigo_ciiu',
                'responsable_iva',
                'gran_contribuyente',
                'autorretenedor'
            )
        }),
        ('Información de Contacto', {
            'fields': (
                'pais',
                'departamento',
                'ciudad',
                'direccion',
                'codigo_postal',
                'telefono_principal',
                'telefono_secundario',
                'email_principal',
                'email_secundario',
                'email_facturacion',
                'sitio_web',
                'horario_atencion'
            )
        }),
        ('Información Bancaria', {
            'fields': ('banco', 'tipo_cuenta', 'numero_cuenta', 'titular_cuenta'),
            'classes': ('collapse',)
        }),
        ('Información Comercial', {
            'fields': (
                'tiempo_entrega_promedio',
                'condiciones_pago',
                'monto_minimo_pedido',
                'descuento_pronto_pago',
                'acepta_credito',
                'metodos_pago_aceptados',
                'calificacion'
            ),
            'classes': ('collapse',)
        }),
        ('Observaciones', {
            'fields': ('notas_internas', 'observaciones'),
            'classes': ('collapse',)
        }),
        ('Control', {
            'fields': ('estado', 'fecha_registro', 'fecha_modificacion')
        }),
    )
    
    readonly_fields = ['fecha_registro', 'fecha_modificacion']


# =====================================================
# ADMIN PARA CONTACTOS - FASE 3
# =====================================================

@admin.register(ContactoProveedor)
class ContactoProveedorAdmin(admin.ModelAdmin):
    list_display = [
        'get_nombre_completo',
        'cargo',
        'id_proveedor',
        'area_responsabilidad',
        'telefono_movil',
        'email',
        'es_contacto_principal',
        'activo'
    ]
    list_filter = ['es_contacto_principal', 'activo', 'area_responsabilidad']
    search_fields = [
        'nombres',
        'apellidos',
        'cargo',
        'email',
        'id_proveedor__razon_social'
    ]
    ordering = ['-es_contacto_principal', 'nombres']
    
    fieldsets = (
        ('Proveedor', {
            'fields': ('id_proveedor',)
        }),
        ('Información Personal', {
            'fields': ('nombres', 'apellidos', 'cargo', 'area_responsabilidad')
        }),
        ('Datos de Contacto', {
            'fields': ('telefono_fijo', 'telefono_movil', 'email')
        }),
        ('Configuración', {
            'fields': ('es_contacto_principal', 'activo')
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_registro', 'fecha_modificacion']
    
    def get_nombre_completo(self, obj):
        """Mostrar nombre completo"""
        return obj.get_nombre_completo()
    get_nombre_completo.short_description = 'Nombre Completo'


# =====================================================
# ADMIN PARA DOCUMENTOS - FASE 4
# =====================================================

@admin.register(DocumentoProveedor)
class DocumentoProveedorAdmin(admin.ModelAdmin):
    list_display = [
        'id_proveedor',
        'id_tipo_documento',
        'numero_documento',
        'fecha_emision',
        'fecha_vencimiento',
        'estado_documento',
        'dias_restantes',
        'fecha_carga'
    ]
    list_filter = ['estado_documento', 'id_tipo_documento', 'fecha_emision']
    search_fields = [
        'id_proveedor__razon_social',
        'id_tipo_documento__nombre_tipo_documento',
        'numero_documento'
    ]
    ordering = ['-fecha_carga']
    date_hierarchy = 'fecha_carga'
    
    fieldsets = (
        ('Proveedor y Tipo', {
            'fields': ('id_proveedor', 'id_tipo_documento')
        }),
        ('Archivo', {
            'fields': ('archivo', 'nombre_archivo_original')
        }),
        ('Información del Documento', {
            'fields': (
                'numero_documento',
                'fecha_emision',
                'fecha_vencimiento',
                'entidad_emisora',
                'estado_documento'
            )
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        }),
        ('Control', {
            'fields': ('fecha_carga', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['nombre_archivo_original', 'fecha_carga', 'fecha_modificacion']
    
    def dias_restantes(self, obj):
        """Mostrar días restantes para vencimiento"""
        dias = obj.get_dias_para_vencer()
        if dias is None:
            return 'N/A'
        elif dias < 0:
            return f'Vencido hace {abs(dias)} días'
        else:
            return f'{dias} días'
    dias_restantes.short_description = 'Días para vencimiento'


# =====================================================
# ADMIN PARA PRODUCTOS/SERVICIOS - FASE 5
# =====================================================

@admin.register(ProductoServicioProveedor)
class ProductoServicioProveedorAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'id_proveedor',
        'tipo',
        'sku_codigo',
        'precio_formateado',
        'unidad_medida',
        'disponibilidad',
        'activo',
        'fecha_registro'
    ]
    list_filter = ['tipo', 'disponible', 'activo', 'moneda', 'unidad_medida']
    search_fields = [
        'nombre',
        'descripcion',
        'sku_codigo',
        'marca',
        'id_proveedor__razon_social'
    ]
    ordering = ['nombre']
    date_hierarchy = 'fecha_registro'
    
    fieldsets = (
        ('Proveedor y Clasificación', {
            'fields': ('id_proveedor', 'tipo', 'nombre')
        }),
        ('Información Básica', {
            'fields': (
                'descripcion',
                'sku_codigo',
                'marca',
                'unidad_medida'
            )
        }),
        ('Precios', {
            'fields': (
                'precio_unitario',
                'moneda',
                'precio_especial',
                'descuento_porcentaje',
                'fecha_ultima_actualizacion_precio'
            )
        }),
        ('Condiciones Comerciales', {
            'fields': (
                'cantidad_minima',
                'tiempo_entrega_dias',
                'disponible',
                'stock_disponible'
            )
        }),
        ('Especificaciones', {
            'fields': ('especificaciones_tecnicas',),
            'classes': ('collapse',)
        }),
        ('Observaciones y Estado', {
            'fields': ('observaciones', 'activo'),
            'classes': ('collapse',)
        }),
        ('Control', {
            'fields': ('fecha_registro', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_registro', 'fecha_modificacion', 'fecha_ultima_actualizacion_precio']
    
    def precio_formateado(self, obj):
        """Mostrar precio formateado"""
        return obj.get_precio_formateado()
    precio_formateado.short_description = 'Precio'
    
    def disponibilidad(self, obj):
        """Mostrar disponibilidad"""
        return obj.get_texto_disponibilidad()
    disponibilidad.short_description = 'Disponibilidad'