"""
Configuración del Admin de Django para el módulo de Inventario de Carpas
American Carpas 1 SAS

Autor: Mario - Universidad La Gran Colombia
Versión: 2.0
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    # Catálogos Base
    UbicacionAlmacen,
    # Catálogos Lonas
    TipoLona, AnchoLona, ColorLona, TratamientoLona,
    # Catálogos Estructura
    TipoEstructura, MedidaTubo, Calibre, MaterialEstructura, AcabadoEstructura,
    # Catálogos Accesorios
    TipoAccesorio,
    # Inventarios
    InventarioLona, InventarioEstructura, InventarioAccesorio,
    # Órdenes de Producción
    OrdenProduccion, OrdenProduccionItem,
    OrdenProduccionLona, OrdenProduccionEstructura, OrdenProduccionAccesorio,
    # Historial
    HistorialInventario,
)


# =============================================================================
# CATÁLOGOS BASE
# =============================================================================

@admin.register(UbicacionAlmacen)
class UbicacionAlmacenAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'bodega', 'zona', 'estante', 'nivel', 'activo']
    list_filter = ['bodega', 'zona', 'activo']
    search_fields = ['codigo', 'nombre', 'bodega']
    list_editable = ['activo']
    ordering = ['bodega', 'zona', 'estante', 'nivel']
    
    fieldsets = (
        ('Identificación', {
            'fields': ('codigo', 'nombre')
        }),
        ('Ubicación Física', {
            'fields': ('bodega', 'zona', 'estante', 'nivel')
        }),
        ('Información Adicional', {
            'fields': ('capacidad_descripcion', 'activo')
        }),
    )


# =============================================================================
# CATÁLOGOS - LONAS
# =============================================================================

@admin.register(TipoLona)
class TipoLonaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['codigo', 'nombre']
    list_editable = ['activo']


@admin.register(AnchoLona)
class AnchoLonaAdmin(admin.ModelAdmin):
    list_display = ['valor_metros', 'descripcion', 'activo']
    list_filter = ['activo']
    list_editable = ['activo']
    ordering = ['valor_metros']


@admin.register(ColorLona)
class ColorLonaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'color_preview', 'codigo_hex', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']
    list_editable = ['activo']
    
    def color_preview(self, obj):
        if obj.codigo_hex:
            return format_html(
                '<span style="background-color: {}; padding: 5px 20px; border: 1px solid #ccc;">&nbsp;</span>',
                obj.codigo_hex
            )
        return '-'
    color_preview.short_description = 'Vista Previa'


@admin.register(TratamientoLona)
class TratamientoLonaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['codigo', 'nombre']
    list_editable = ['activo']


# =============================================================================
# CATÁLOGOS - ESTRUCTURA
# =============================================================================

@admin.register(TipoEstructura)
class TipoEstructuraAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['codigo', 'nombre']
    list_editable = ['activo']


@admin.register(MedidaTubo)
class MedidaTuboAdmin(admin.ModelAdmin):
    list_display = ['valor_medida', 'valor_pulgadas', 'descripcion', 'activo']
    list_filter = ['activo']
    search_fields = ['valor_medida']
    list_editable = ['activo']
    ordering = ['valor_pulgadas']


@admin.register(Calibre)
class CalibreAdmin(admin.ModelAdmin):
    list_display = ['valor_calibre', 'espesor_mm', 'descripcion', 'activo']
    list_filter = ['activo']
    list_editable = ['activo']
    ordering = ['valor_calibre']


@admin.register(MaterialEstructura)
class MaterialEstructuraAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['codigo', 'nombre']
    list_editable = ['activo']


@admin.register(AcabadoEstructura)
class AcabadoEstructuraAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['codigo', 'nombre']
    list_editable = ['activo']


# =============================================================================
# CATÁLOGOS - ACCESORIOS
# =============================================================================

@admin.register(TipoAccesorio)
class TipoAccesorioAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'unidad_medida', 'activo']
    list_filter = ['activo', 'unidad_medida']
    search_fields = ['codigo', 'nombre']
    list_editable = ['activo']


# =============================================================================
# INVENTARIO - LONAS
# =============================================================================

@admin.register(InventarioLona)
class InventarioLonaAdmin(admin.ModelAdmin):
    list_display = [
        'codigo_rollo', 'tipo_lona', 'ancho_lona', 'color_lona',
        'metros_disponibles_display', 'metros_iniciales', 
        'ubicacion', 'estado_badge', 'activo'
    ]
    list_filter = [
        'tipo_lona', 'ancho_lona', 'color_lona', 'tratamiento',
        'ubicacion__bodega', 'estado', 'activo'
    ]
    search_fields = ['codigo_rollo', 'lote_serial', 'observaciones']
    readonly_fields = [
        'codigo_rollo', 'codigo_qr', 'metros_utilizados', 
        'metros_reales_disponibles', 'valor_inventario', 'porcentaje_disponible',
        'fecha_creacion', 'fecha_actualizacion'
    ]
    date_hierarchy = 'fecha_ingreso'
    autocomplete_fields = ['proveedor', 'ubicacion']
    list_editable = ['activo']
    
    fieldsets = (
        ('Identificación', {
            'fields': ('codigo_rollo', 'codigo_qr')
        }),
        ('Características', {
            'fields': ('tipo_lona', 'ancho_lona', 'color_lona', 'tratamiento', 'gramaje')
        }),
        ('Control de Metraje', {
            'fields': (
                'metros_iniciales', 'metros_disponibles', 'metros_reservados',
                'metros_minimo_alerta', 'metros_utilizados', 'metros_reales_disponibles',
                'porcentaje_disponible'
            )
        }),
        ('Costos', {
            'fields': ('costo_por_metro', 'valor_inventario')
        }),
        ('Ubicación y Origen', {
            'fields': ('ubicacion', 'proveedor', 'lote_serial', 'numero_factura')
        }),
        ('Fechas', {
            'fields': ('fecha_ingreso', 'fecha_fabricacion', 'fecha_ultima_salida', 'garantia_meses')
        }),
        ('Estado y Control', {
            'fields': ('estado', 'imagen', 'observaciones', 'activo')
        }),
        ('Auditoría', {
            'fields': ('creado_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def metros_disponibles_display(self, obj):
        color = 'green' if obj.metros_disponibles > obj.metros_minimo_alerta else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} m</span>',
            color, obj.metros_disponibles
        )
    metros_disponibles_display.short_description = 'Disponibles'
    metros_disponibles_display.admin_order_field = 'metros_disponibles'
    
    def estado_badge(self, obj):
        colors = {
            'DISPONIBLE': 'success',
            'EN_USO': 'primary',
            'RESERVADO': 'warning',
            'AGOTADO': 'secondary',
            'BAJA': 'danger',
        }
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            colors.get(obj.estado, 'secondary'),
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    
    def metros_utilizados(self, obj):
        return f"{obj.metros_utilizados} m"
    metros_utilizados.short_description = 'Metros Utilizados'
    
    def metros_reales_disponibles(self, obj):
        return f"{obj.metros_reales_disponibles} m"
    metros_reales_disponibles.short_description = 'Disponibles Reales'
    
    def valor_inventario(self, obj):
        return f"${obj.valor_inventario:,.2f}"
    valor_inventario.short_description = 'Valor Inventario'
    
    def porcentaje_disponible(self, obj):
        return f"{obj.porcentaje_disponible}%"
    porcentaje_disponible.short_description = '% Disponible'


# =============================================================================
# INVENTARIO - ESTRUCTURA
# =============================================================================

@admin.register(InventarioEstructura)
class InventarioEstructuraAdmin(admin.ModelAdmin):
    list_display = [
        'codigo_lote', 'tipo_estructura', 'medida_tubo', 'calibre',
        'cantidad_display', 'ubicacion', 'estado', 'activo'
    ]
    list_filter = [
        'tipo_estructura', 'medida_tubo', 'calibre', 'material',
        'tipo_control', 'ubicacion__bodega', 'estado', 'activo'
    ]
    search_fields = ['codigo_lote', 'lote_serial']
    readonly_fields = ['codigo_lote', 'codigo_qr', 'valor_inventario', 'fecha_creacion', 'fecha_actualizacion']
    date_hierarchy = 'fecha_ingreso'
    autocomplete_fields = ['proveedor', 'ubicacion']
    list_editable = ['activo']
    
    fieldsets = (
        ('Identificación', {
            'fields': ('codigo_lote', 'codigo_qr')
        }),
        ('Características', {
            'fields': ('tipo_estructura', 'medida_tubo', 'calibre', 'material', 'acabado', 'peso_por_metro')
        }),
        ('Tipo de Control', {
            'fields': ('tipo_control',)
        }),
        ('Control por Metros', {
            'fields': ('metros_iniciales', 'metros_disponibles', 'metros_reservados', 'metros_minimo_alerta'),
            'classes': ('collapse',)
        }),
        ('Control por Piezas', {
            'fields': ('longitud_pieza', 'piezas_iniciales', 'piezas_disponibles', 'piezas_reservadas', 'piezas_minimo_alerta'),
            'classes': ('collapse',)
        }),
        ('Costos', {
            'fields': ('costo_por_metro', 'costo_por_pieza', 'valor_inventario')
        }),
        ('Ubicación y Origen', {
            'fields': ('ubicacion', 'proveedor', 'lote_serial', 'numero_factura')
        }),
        ('Fechas', {
            'fields': ('fecha_ingreso', 'fecha_ultima_salida')
        }),
        ('Estado y Control', {
            'fields': ('estado', 'imagen', 'observaciones', 'activo')
        }),
        ('Auditoría', {
            'fields': ('creado_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def cantidad_display(self, obj):
        if obj.tipo_control == 'METROS':
            return f"{obj.metros_disponibles} m"
        return f"{obj.piezas_disponibles} pzas"
    cantidad_display.short_description = 'Cantidad'
    
    def valor_inventario(self, obj):
        return f"${obj.valor_inventario:,.2f}"
    valor_inventario.short_description = 'Valor Inventario'


# =============================================================================
# INVENTARIO - ACCESORIOS
# =============================================================================

@admin.register(InventarioAccesorio)
class InventarioAccesorioAdmin(admin.ModelAdmin):
    list_display = [
        'codigo', 'nombre', 'tipo_accesorio',
        'cantidad_disponible', 'cantidad_inicial', 'ubicacion', 'estado', 'activo'
    ]
    list_filter = ['tipo_accesorio', 'ubicacion__bodega', 'estado', 'activo']
    search_fields = ['codigo', 'nombre', 'descripcion']
    readonly_fields = ['codigo', 'codigo_qr', 'valor_inventario', 'fecha_creacion', 'fecha_actualizacion']
    date_hierarchy = 'fecha_ingreso'
    autocomplete_fields = ['proveedor', 'ubicacion']
    list_editable = ['activo']
    
    fieldsets = (
        ('Identificación', {
            'fields': ('codigo', 'codigo_qr')
        }),
        ('Características', {
            'fields': ('tipo_accesorio', 'nombre', 'descripcion', 'especificaciones')
        }),
        ('Control de Cantidad', {
            'fields': ('cantidad_inicial', 'cantidad_disponible', 'cantidad_reservada', 'cantidad_minima_alerta')
        }),
        ('Costos', {
            'fields': ('costo_unitario', 'valor_inventario')
        }),
        ('Ubicación y Origen', {
            'fields': ('ubicacion', 'proveedor', 'lote_serial')
        }),
        ('Fechas', {
            'fields': ('fecha_ingreso', 'fecha_ultima_salida')
        }),
        ('Estado y Control', {
            'fields': ('estado', 'imagen', 'observaciones', 'activo')
        }),
        ('Auditoría', {
            'fields': ('creado_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def valor_inventario(self, obj):
        return f"${obj.valor_inventario:,.2f}"
    valor_inventario.short_description = 'Valor Inventario'


# =============================================================================
# ÓRDENES DE PRODUCCIÓN
# =============================================================================

class OrdenProduccionItemInline(admin.TabularInline):
    model = OrdenProduccionItem
    extra = 1
    fields = [
        'numero_linea', 'cantidad', 'tipo_producto', 'dimensiones',
        'color_estructura', 'color_lona', 'descripcion_completa'
    ]


class OrdenProduccionLonaInline(admin.TabularInline):
    model = OrdenProduccionLona
    extra = 0
    fields = ['lona', 'metros_requeridos', 'metros_utilizados', 'cortado_por', 'fecha_corte', 'estado']
    readonly_fields = ['metros_utilizados']
    autocomplete_fields = ['lona']


class OrdenProduccionEstructuraInline(admin.TabularInline):
    model = OrdenProduccionEstructura
    extra = 0
    fields = [
        'estructura', 'metros_requeridos', 'metros_utilizados',
        'piezas_requeridas', 'piezas_utilizadas', 'estado'
    ]
    readonly_fields = ['metros_utilizados', 'piezas_utilizadas']
    autocomplete_fields = ['estructura']


class OrdenProduccionAccesorioInline(admin.TabularInline):
    model = OrdenProduccionAccesorio
    extra = 0
    fields = ['accesorio', 'cantidad_requerida', 'cantidad_entregada', 'estado']
    readonly_fields = ['cantidad_entregada']
    autocomplete_fields = ['accesorio']


@admin.register(OrdenProduccion)
class OrdenProduccionAdmin(admin.ModelAdmin):
    list_display = [
        'numero_orden_display', 'cliente', 'fecha_entrega_requerida',
        'fases_display', 'estado_badge', 'es_urgente_display', 'porcentaje_avance_display'
    ]
    list_filter = [
        'estado', 'es_urgente', 'año', 'estructura_fabricada', 
        'estructura_pintada', 'lona_fabricada', 'terminada'
    ]
    search_fields = ['numero_orden', 'cliente', 'ubicacion_entrega']
    readonly_fields = [
        'codigo_completo', 'porcentaje_avance',
        'fecha_creacion', 'fecha_actualizacion'
    ]
    date_hierarchy = 'fecha_orden'
    autocomplete_fields = ['proyecto']
    
    inlines = [
        OrdenProduccionItemInline,
        OrdenProduccionLonaInline,
        OrdenProduccionEstructuraInline,
        OrdenProduccionAccesorioInline,
    ]
    
    fieldsets = (
        ('Identificación', {
            'fields': ('numero_orden', 'año', 'codigo_completo')
        }),
        ('Información General', {
            'fields': ('fecha_orden', 'fecha_entrega_requerida', 'proyecto', 'cliente', 'ubicacion_entrega')
        }),
        ('Control de Fases', {
            'fields': (
                ('estructura_fabricada', 'fecha_estructura_fabricada'),
                ('estructura_pintada', 'fecha_estructura_pintada'),
                ('lona_fabricada', 'fecha_lona_fabricada'),
                ('terminada', 'fecha_terminada'),
            )
        }),
        ('Autorización', {
            'fields': ('solicitado_por', 'autorizado_por', 'fecha_autorizacion')
        }),
        ('Estado y Prioridad', {
            'fields': ('estado', 'es_urgente', 'prioridad', 'porcentaje_avance')
        }),
        ('Fechas de Ejecución', {
            'fields': ('fecha_inicio_produccion', 'fecha_fin_produccion'),
            'classes': ('collapse',)
        }),
        ('Observaciones', {
            'fields': ('observaciones', 'activo')
        }),
        ('Auditoría', {
            'fields': ('creado_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def numero_orden_display(self, obj):
        return f"OP-{obj.numero_orden}"
    numero_orden_display.short_description = '# Orden'
    numero_orden_display.admin_order_field = 'numero_orden'
    
    def fases_display(self, obj):
        checks = [
            ('E.Fab', obj.estructura_fabricada),
            ('E.Pin', obj.estructura_pintada),
            ('Lona', obj.lona_fabricada),
            ('Term', obj.terminada),
        ]
        html = ''
        for label, value in checks:
            icon = '✓' if value else '○'
            color = 'green' if value else '#ccc'
            html += f'<span style="color:{color}; margin-right:5px;" title="{label}">{icon}</span>'
        return format_html(html)
    fases_display.short_description = 'Fases'
    
    def estado_badge(self, obj):
        colors = {
            'BORRADOR': 'secondary',
            'PENDIENTE': 'warning',
            'AUTORIZADA': 'info',
            'EN_PROCESO': 'primary',
            'COMPLETADA': 'success',
            'CANCELADA': 'danger',
        }
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            colors.get(obj.estado, 'secondary'),
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    
    def es_urgente_display(self, obj):
        if obj.es_urgente:
            return format_html('<span style="color: red; font-weight: bold;">⚠ URGENTE</span>')
        return '-'
    es_urgente_display.short_description = 'Urgente'
    
    def porcentaje_avance_display(self, obj):
        pct = obj.porcentaje_avance
        color = 'success' if pct == 100 else 'primary' if pct >= 50 else 'warning'
        return format_html(
            '<div class="progress" style="width:80px;height:20px;">'
            '<div class="progress-bar bg-{}" style="width:{}%">{}</div>'
            '</div>',
            color, pct, f'{pct}%'
        )
    porcentaje_avance_display.short_description = 'Avance'
    
    def codigo_completo(self, obj):
        return obj.codigo_completo
    codigo_completo.short_description = 'Código Completo'
    
    def porcentaje_avance(self, obj):
        return f"{obj.porcentaje_avance}%"
    porcentaje_avance.short_description = '% Avance'


@admin.register(OrdenProduccionItem)
class OrdenProduccionItemAdmin(admin.ModelAdmin):
    list_display = [
        'orden', 'numero_linea', 'cantidad', 'tipo_producto', 
        'dimensiones', 'color_lona', 'color_estructura'
    ]
    list_filter = ['orden__año', 'tipo_producto']
    search_fields = ['orden__numero_orden', 'descripcion_completa', 'tipo_producto']
    autocomplete_fields = ['orden']


# =============================================================================
# HISTORIAL DE INVENTARIO
# =============================================================================

@admin.register(HistorialInventario)
class HistorialInventarioAdmin(admin.ModelAdmin):
    list_display = [
        'fecha_movimiento', 'tipo_movimiento_badge', 'tipo_inventario',
        'item_display', 'cantidad_movimiento', 'unidad_medida',
        'documento_referencia', 'ejecutado_por'
    ]
    list_filter = ['tipo_movimiento', 'tipo_inventario', 'fecha_movimiento']
    search_fields = ['documento_referencia', 'motivo', 'observaciones']
    readonly_fields = ['fecha_creacion']
    date_hierarchy = 'fecha_movimiento'
    
    fieldsets = (
        ('Movimiento', {
            'fields': ('fecha_movimiento', 'tipo_movimiento', 'tipo_inventario')
        }),
        ('Inventario', {
            'fields': ('lona', 'estructura', 'accesorio')
        }),
        ('Referencia', {
            'fields': ('orden_produccion',)
        }),
        ('Cantidades', {
            'fields': ('cantidad_anterior', 'cantidad_movimiento', 'cantidad_nueva', 'unidad_medida')
        }),
        ('Responsables', {
            'fields': ('ejecutado_por', 'autorizado_por')
        }),
        ('Documentación', {
            'fields': ('documento_referencia', 'motivo', 'observaciones')
        }),
        ('Auditoría', {
            'fields': ('registrado_por', 'fecha_creacion'),
            'classes': ('collapse',)
        }),
    )
    
    def tipo_movimiento_badge(self, obj):
        colors = {
            'ENTRADA': 'success',
            'SALIDA': 'danger',
            'AJUSTE_POSITIVO': 'info',
            'AJUSTE_NEGATIVO': 'warning',
            'RESERVA': 'primary',
            'LIBERACION': 'secondary',
            'DEVOLUCION': 'info',
            'BAJA': 'dark',
        }
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            colors.get(obj.tipo_movimiento, 'secondary'),
            obj.get_tipo_movimiento_display()
        )
    tipo_movimiento_badge.short_description = 'Tipo'
    
    def item_display(self, obj):
        item = obj.item_inventario
        if item:
            if hasattr(item, 'codigo_rollo'):
                return item.codigo_rollo
            elif hasattr(item, 'codigo_lote'):
                return item.codigo_lote
            elif hasattr(item, 'codigo'):
                return item.codigo
        return '-'
    item_display.short_description = 'Ítem'


# =============================================================================
# CONFIGURACIÓN DE BÚSQUEDA PARA AUTOCOMPLETE
# =============================================================================

# Agregar search_fields a modelos referenciados por autocomplete
UbicacionAlmacen.search_fields = ['codigo', 'nombre', 'bodega']
InventarioLona.search_fields = ['codigo_rollo', 'lote_serial']
InventarioEstructura.search_fields = ['codigo_lote', 'lote_serial']
InventarioAccesorio.search_fields = ['codigo', 'nombre']