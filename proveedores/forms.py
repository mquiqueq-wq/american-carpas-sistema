from django import forms
from .models import TipoProveedor, CategoriaProveedor, TipoDocumentoProveedor


# =====================================================
# WIDGETS COMUNES
# =====================================================
TEXT_INPUT = forms.TextInput(attrs={"class": "form-control"})
SELECT = forms.Select(attrs={"class": "form-select"})
NUMBER_INPUT = forms.NumberInput(attrs={"class": "form-control"})
TEXTAREA = forms.Textarea(attrs={"class": "form-control", "rows": 3})
CHECKBOX = forms.CheckboxInput(attrs={"class": "form-check-input"})


# =====================================================
# FORMULARIOS DE CATÁLOGOS - FASE 1
# =====================================================


class TipoProveedorForm(forms.ModelForm):
    """
    Formulario para crear/editar tipos de proveedores
    """
    nombre_tipo = forms.CharField(
        label='Nombre del Tipo',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Fabricante, Distribuidor, Importador'
        })
    )
    
    descripcion = forms.CharField(
        label='Descripción',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descripción detallada del tipo de proveedor...'
        })
    )
    
    requiere_certificaciones = forms.BooleanField(
        label='¿Requiere certificaciones especiales?',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    icono_bootstrap = forms.CharField(
        label='Icono Bootstrap',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: bi-building, bi-truck, bi-globe'
        }),
        help_text='Nombre del icono de Bootstrap Icons'
    )
    
    orden_visualizacion = forms.IntegerField(
        label='Orden de visualización',
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0'
        }),
        help_text='Orden en que se muestra (menor = primero)'
    )
    
    activo = forms.BooleanField(
        label='Activo',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    class Meta:
        model = TipoProveedor
        fields = [
            'nombre_tipo',
            'descripcion',
            'requiere_certificaciones',
            'icono_bootstrap',
            'orden_visualizacion',
            'activo'
        ]


class CategoriaProveedorForm(forms.ModelForm):
    """
    Formulario para crear/editar categorías de proveedores
    """
    nombre_categoria = forms.CharField(
        label='Nombre de la Categoría',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Lonas y Telas, Estructuras Metálicas'
        })
    )
    
    descripcion = forms.CharField(
        label='Descripción',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descripción de los productos/servicios de esta categoría...'
        })
    )
    
    categoria_padre = forms.ModelChoiceField(
        label='Categoría Padre (opcional)',
        queryset=CategoriaProveedor.objects.filter(activo=True),
        required=False,
        empty_label='-- Sin categoría padre (categoría principal) --',
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        help_text='Para crear una subcategoría'
    )
    
    color_badge = forms.ChoiceField(
        label='Color del Badge',
        choices=[
            ('primary', 'Azul (Primary)'),
            ('success', 'Verde (Success)'),
            ('danger', 'Rojo (Danger)'),
            ('warning', 'Amarillo (Warning)'),
            ('info', 'Cian (Info)'),
            ('secondary', 'Gris (Secondary)'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    icono_bootstrap = forms.CharField(
        label='Icono Bootstrap',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: bi-basket, bi-box, bi-tools'
        }),
        help_text='Nombre del icono de Bootstrap Icons'
    )
    
    orden_visualizacion = forms.IntegerField(
        label='Orden de visualización',
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0'
        }),
        help_text='Orden en que se muestra (menor = primero)'
    )
    
    activo = forms.BooleanField(
        label='Activo',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    class Meta:
        model = CategoriaProveedor
        fields = [
            'nombre_categoria',
            'descripcion',
            'categoria_padre',
            'color_badge',
            'icono_bootstrap',
            'orden_visualizacion',
            'activo'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando, excluir la categoría actual de las opciones de padre
        # para evitar referencias circulares
        if self.instance.pk:
            self.fields['categoria_padre'].queryset = CategoriaProveedor.objects.filter(
                activo=True
            ).exclude(pk=self.instance.pk)


class TipoDocumentoProveedorForm(forms.ModelForm):
    """
    Formulario para crear/editar tipos de documentos de proveedores
    """
    nombre_tipo_documento = forms.CharField(
        label='Nombre del Tipo de Documento',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: RUT, Cámara de Comercio, Certificado ISO'
        })
    )
    
    descripcion = forms.CharField(
        label='Descripción',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descripción detallada del tipo de documento...'
        })
    )
    
    es_obligatorio = forms.BooleanField(
        label='¿Es obligatorio?',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        help_text='Marcar si es obligatorio para todos los proveedores'
    )
    
    requiere_vigencia = forms.BooleanField(
        label='¿Requiere control de vigencia?',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'id_requiere_vigencia'
        }),
        help_text='Marcar si el documento tiene fecha de vencimiento'
    )
    
    dias_alerta_vencimiento = forms.IntegerField(
        label='Días de alerta antes del vencimiento',
        initial=30,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'id': 'id_dias_alerta'
        }),
        help_text='Días antes del vencimiento para generar alerta'
    )
    
    icono_bootstrap = forms.CharField(
        label='Icono Bootstrap',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: bi-file-earmark-text, bi-card-checklist'
        }),
        help_text='Nombre del icono de Bootstrap Icons'
    )
    
    orden_visualizacion = forms.IntegerField(
        label='Orden de visualización',
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0'
        }),
        help_text='Orden en que se muestra (menor = primero)'
    )
    
    activo = forms.BooleanField(
        label='Activo',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    class Meta:
        model = TipoDocumentoProveedor
        fields = [
            'nombre_tipo_documento',
            'descripcion',
            'es_obligatorio',
            'requiere_vigencia',
            'dias_alerta_vencimiento',
            'icono_bootstrap',
            'orden_visualizacion',
            'activo'
        ]
