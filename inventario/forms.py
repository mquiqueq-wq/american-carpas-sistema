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