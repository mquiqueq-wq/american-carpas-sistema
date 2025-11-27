"""
Formularios para el módulo de Inventario de Carpas
American Carpas 1 SAS

Versión: 2.0 - Fase 2: Catálogos Completos
"""

from django import forms
from .models import (
    # Catálogos Base
    UbicacionAlmacen,
    # Catálogos Lonas
    TipoLona, AnchoLona, ColorLona, TratamientoLona,
    # Catálogos Estructura
    TipoEstructura, MedidaTubo, Calibre, MaterialEstructura, AcabadoEstructura,
    # Catálogos Accesorios
    TipoAccesorio,
    # Inventarios Principales
    InventarioLona, InventarioEstructura, InventarioAccesorio,
    # Órdenes de Producción
    OrdenProduccion, OrdenProduccionItem,
)


# =============================================================================
# FORMULARIOS - UBICACIÓN DE ALMACÉN
# =============================================================================

class UbicacionAlmacenForm(forms.ModelForm):
    """Formulario para ubicaciones de almacén"""
    
    class Meta:
        model = UbicacionAlmacen
        fields = [
            'codigo', 'nombre', 'bodega', 'zona', 
            'estante', 'nivel', 'capacidad_descripcion', 'activo'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: BOD-A-E3-N2'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Bodega A - Estante 3 - Nivel 2'
            }),
            'bodega': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Bodega Principal'
            }),
            'zona': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Zona A'
            }),
            'estante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Estante 3'
            }),
            'nivel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Nivel 2'
            }),
            'capacidad_descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Rollos grandes'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


# =============================================================================
# FORMULARIOS - CATÁLOGOS DE LONAS
# =============================================================================

class TipoLonaForm(forms.ModelForm):
    """Formulario para tipos de lona"""
    
    class Meta:
        model = TipoLona
        fields = ['codigo', 'nombre', 'descripcion', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: PVC'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Lona PVC'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del tipo de lona...'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class AnchoLonaForm(forms.ModelForm):
    """Formulario para anchos de lona"""
    
    class Meta:
        model = AnchoLona
        fields = ['valor_metros', 'descripcion', 'activo']
        widgets = {
            'valor_metros': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 2.50',
                'step': '0.01'
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Ancho estándar grande'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ColorLonaForm(forms.ModelForm):
    """Formulario para colores de lona"""
    
    class Meta:
        model = ColorLona
        fields = ['nombre', 'codigo_hex', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Blanco'
            }),
            'codigo_hex': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: #FFFFFF',
                'type': 'color'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class TratamientoLonaForm(forms.ModelForm):
    """Formulario para tratamientos de lona"""
    
    class Meta:
        model = TratamientoLona
        fields = ['codigo', 'nombre', 'descripcion', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: IMP'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Impermeabilizado'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del tratamiento...'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


# =============================================================================
# FORMULARIOS - CATÁLOGOS DE ESTRUCTURA
# =============================================================================

class TipoEstructuraForm(forms.ModelForm):
    """Formulario para tipos de estructura"""
    
    class Meta:
        model = TipoEstructura
        fields = ['codigo', 'nombre', 'descripcion', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: TUB-RED'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Tubo Redondo'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del tipo...'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class MedidaTuboForm(forms.ModelForm):
    """Formulario para medidas de tubo"""
    
    class Meta:
        model = MedidaTubo
        fields = ['valor_medida', 'valor_pulgadas', 'descripcion', 'activo']
        widgets = {
            'valor_medida': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 2 pulgadas'
            }),
            'valor_pulgadas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 2.00',
                'step': '0.01'
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción opcional'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class CalibreForm(forms.ModelForm):
    """Formulario para calibres"""
    
    class Meta:
        model = Calibre
        fields = ['valor_calibre', 'espesor_mm', 'descripcion', 'activo']
        widgets = {
            'valor_calibre': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 16',
                'step': '0.01'
            }),
            'espesor_mm': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1.52',
                'step': '0.001'
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción opcional'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class MaterialEstructuraForm(forms.ModelForm):
    """Formulario para materiales de estructura"""
    
    class Meta:
        model = MaterialEstructura
        fields = ['codigo', 'nombre', 'descripcion', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: AC-GAL'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Acero Galvanizado'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del material...'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class AcabadoEstructuraForm(forms.ModelForm):
    """Formulario para acabados de estructura"""
    
    class Meta:
        model = AcabadoEstructura
        fields = ['codigo', 'nombre', 'descripcion', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: PINT-ELEC'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Pintura Electrostática'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del acabado...'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


# =============================================================================
# FORMULARIOS - CATÁLOGOS DE ACCESORIOS
# =============================================================================

class TipoAccesorioForm(forms.ModelForm):
    """Formulario para tipos de accesorio"""
    
    class Meta:
        model = TipoAccesorio
        fields = ['codigo', 'nombre', 'descripcion', 'unidad_medida', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: TEN'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Tensor'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del tipo de accesorio...'
            }),
            'unidad_medida': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: unidad, metro, rollo'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


# =============================================================================
# FORMULARIOS - INVENTARIO DE LONAS
# =============================================================================

class InventarioLonaForm(forms.ModelForm):
    """Formulario para inventario de lonas"""
    
    class Meta:
        model = InventarioLona
        fields = [
            'tipo_lona', 'ancho_lona', 'color_lona', 'tratamiento',
            'gramaje', 'metros_iniciales', 'metros_disponibles',
            'metros_reservados', 'metros_minimo_alerta',
            'costo_por_metro', 'ubicacion', 'proveedor',
            'lote_serial', 'numero_factura', 'fecha_ingreso',
            'fecha_fabricacion', 'garantia_meses',
            'estado', 'imagen', 'observaciones', 'activo'
        ]
        widgets = {
            'tipo_lona': forms.Select(attrs={'class': 'form-select'}),
            'ancho_lona': forms.Select(attrs={'class': 'form-select'}),
            'color_lona': forms.Select(attrs={'class': 'form-select'}),
            'tratamiento': forms.Select(attrs={'class': 'form-select'}),
            'gramaje': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 650',
                'step': '0.01'
            }),
            'metros_iniciales': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'metros_disponibles': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'metros_reservados': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'metros_minimo_alerta': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'costo_por_metro': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'ubicacion': forms.Select(attrs={'class': 'form-select'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'lote_serial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de lote o serial'
            }),
            'numero_factura': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de factura'
            }),
            'fecha_ingreso': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fabricacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'garantia_meses': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# =============================================================================
# FORMULARIOS - INVENTARIO DE ESTRUCTURA
# =============================================================================

class InventarioEstructuraForm(forms.ModelForm):
    """Formulario para inventario de estructura"""
    
    class Meta:
        model = InventarioEstructura
        fields = [
            'tipo_estructura', 'medida_tubo', 'calibre', 'material', 'acabado',
            'peso_por_metro', 'tipo_control',
            'metros_iniciales', 'metros_disponibles', 'metros_reservados', 'metros_minimo_alerta',
            'longitud_pieza', 'piezas_iniciales', 'piezas_disponibles', 'piezas_reservadas', 'piezas_minimo_alerta',
            'costo_por_metro', 'costo_por_pieza',
            'ubicacion', 'proveedor', 'lote_serial', 'numero_factura',
            'fecha_ingreso', 'estado', 'observaciones', 'activo'
        ]
        widgets = {
            'tipo_estructura': forms.Select(attrs={'class': 'form-select'}),
            'medida_tubo': forms.Select(attrs={'class': 'form-select'}),
            'calibre': forms.Select(attrs={'class': 'form-select'}),
            'material': forms.Select(attrs={'class': 'form-select'}),
            'acabado': forms.Select(attrs={'class': 'form-select'}),
            'peso_por_metro': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001'
            }),
            'tipo_control': forms.Select(attrs={'class': 'form-select'}),
            'metros_iniciales': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'metros_disponibles': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'metros_reservados': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'metros_minimo_alerta': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'longitud_pieza': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'piezas_iniciales': forms.NumberInput(attrs={'class': 'form-control'}),
            'piezas_disponibles': forms.NumberInput(attrs={'class': 'form-control'}),
            'piezas_reservadas': forms.NumberInput(attrs={'class': 'form-control'}),
            'piezas_minimo_alerta': forms.NumberInput(attrs={'class': 'form-control'}),
            'costo_por_metro': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'costo_por_pieza': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'ubicacion': forms.Select(attrs={'class': 'form-select'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'lote_serial': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_factura': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# =============================================================================
# FORMULARIOS - INVENTARIO DE ACCESORIOS
# =============================================================================

class InventarioAccesorioForm(forms.ModelForm):
    """Formulario para inventario de accesorios"""
    
    class Meta:
        model = InventarioAccesorio
        fields = [
            'tipo_accesorio', 'nombre', 'descripcion', 'especificaciones',
            'cantidad_inicial', 'cantidad_disponible', 'cantidad_reservada', 'cantidad_minima_alerta',
            'costo_unitario', 'ubicacion', 'proveedor',
            'lote_serial', 'fecha_ingreso', 'imagen',
            'estado', 'observaciones', 'activo'
        ]
        widgets = {
            'tipo_accesorio': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del accesorio'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'especificaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'cantidad_inicial': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_reservada': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_minima_alerta': forms.NumberInput(attrs={'class': 'form-control'}),
            'costo_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'ubicacion': forms.Select(attrs={'class': 'form-select'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'lote_serial': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# =============================================================================
# FORMULARIOS - ÓRDENES DE PRODUCCIÓN
# =============================================================================

class OrdenProduccionForm(forms.ModelForm):
    """Formulario para órdenes de producción"""
    
    class Meta:
        model = OrdenProduccion
        fields = [
            'fecha_orden', 'fecha_entrega_requerida', 'proyecto', 'cliente',
            'ubicacion_entrega', 'solicitado_por', 'es_urgente', 'prioridad',
            'estado', 'observaciones'
        ]
        widgets = {
            'fecha_orden': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_entrega_requerida': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'proyecto': forms.Select(attrs={'class': 'form-select'}),
            'cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del cliente'
            }),
            'ubicacion_entrega': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección de entrega'
            }),
            'solicitado_por': forms.Select(attrs={'class': 'form-select'}),
            'es_urgente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prioridad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5'
            }),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


class OrdenProduccionItemForm(forms.ModelForm):
    """Formulario para ítems de orden de producción"""
    
    class Meta:
        model = OrdenProduccionItem
        fields = [
            'cantidad', 'tipo_producto', 'dimensiones', 'color_estructura',
            'color_lona', 'incluye_cortinas', 'cantidad_cortinas',
            'incluye_logo_techo', 'cantidad_logos_techo',
            'incluye_logo_cortina', 'cantidad_logos_cortina',
            'incluye_faldon', 'incluye_entecho', 'otros_accesorios',
            'descripcion_completa', 'especificaciones_cliente'
        ]
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_producto': forms.Select(attrs={'class': 'form-select'}),
            'dimensiones': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 3x3 MTS, 10x20 MTS'
            }),
            'color_estructura': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Blanco, Azul'
            }),
            'color_lona': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Blanco, Azul'
            }),
            'incluye_cortinas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cantidad_cortinas': forms.NumberInput(attrs={'class': 'form-control'}),
            'incluye_logo_techo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cantidad_logos_techo': forms.NumberInput(attrs={'class': 'form-control'}),
            'incluye_logo_cortina': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cantidad_logos_cortina': forms.NumberInput(attrs={'class': 'form-control'}),
            'incluye_faldon': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'incluye_entecho': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'otros_accesorios': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'descripcion_completa': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción completa del producto...'
            }),
            'especificaciones_cliente': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
        }