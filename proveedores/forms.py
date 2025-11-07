from django import forms
from .models import (
    TipoProveedor, CategoriaProveedor, TipoDocumentoProveedor,
    Proveedor  # FASE 2
)


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


# =====================================================
# FORMULARIO PRINCIPAL - FASE 2
# =====================================================


class ProveedorForm(forms.ModelForm):
    """
    Formulario completo para crear/editar proveedores
    Organizado por secciones lógicas
    """
    
    # ===== IDENTIFICACIÓN BÁSICA =====
    razon_social = forms.CharField(
        label='Razón Social',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre legal de la empresa'
        })
    )
    
    nombre_comercial = forms.CharField(
        label='Nombre Comercial',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre con el que se conoce (opcional)'
        })
    )
    
    tipo_documento = forms.ChoiceField(
        label='Tipo de Documento',
        choices=Proveedor._meta.get_field('tipo_documento').choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    numero_documento = forms.CharField(
        label='Número de Documento',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'NIT o documento sin dígito de verificación'
        })
    )
    
    digito_verificacion = forms.CharField(
        label='Dígito de Verificación',
        max_length=1,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Solo para NIT'
        })
    )
    
    tipo_proveedor = forms.ModelChoiceField(
        label='Tipo de Proveedor',
        queryset=TipoProveedor.objects.filter(activo=True),
        empty_label='-- Seleccione un tipo --',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    categoria_principal = forms.ModelChoiceField(
        label='Categoría Principal',
        queryset=CategoriaProveedor.objects.filter(activo=True, categoria_padre__isnull=True),
        empty_label='-- Seleccione una categoría --',
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Seleccione la categoría principal de productos/servicios'
    )
    
    estado = forms.ChoiceField(
        label='Estado',
        choices=Proveedor._meta.get_field('estado').choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # ===== INFORMACIÓN LEGAL Y TRIBUTARIA =====
    regimen_tributario = forms.ChoiceField(
        label='Régimen Tributario',
        choices=Proveedor._meta.get_field('regimen_tributario').choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    responsabilidad_fiscal = forms.ChoiceField(
        label='Responsabilidad Fiscal',
        choices=Proveedor._meta.get_field('responsabilidad_fiscal').choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    actividad_economica = forms.CharField(
        label='Actividad Económica',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Fabricación de estructuras metálicas'
        })
    )
    
    codigo_ciiu = forms.CharField(
        label='Código CIIU',
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 2511'
        })
    )
    
    pais_origen = forms.CharField(
        label='País de Origen',
        max_length=50,
        initial='Colombia',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    # ===== INFORMACIÓN DE CONTACTO =====
    direccion_principal = forms.CharField(
        label='Dirección Principal',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Calle, número, barrio'
        })
    )
    
    ciudad = forms.CharField(
        label='Ciudad',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Medellín'
        })
    )
    
    departamento = forms.CharField(
        label='Departamento',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Antioquia'
        })
    )
    
    pais = forms.CharField(
        label='País',
        max_length=50,
        initial='Colombia',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    codigo_postal = forms.CharField(
        label='Código Postal',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional'
        })
    )
    
    telefono_principal = forms.CharField(
        label='Teléfono Principal',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: (604) 123-4567'
        })
    )
    
    telefono_secundario = forms.CharField(
        label='Teléfono Secundario',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional'
        })
    )
    
    email_principal = forms.EmailField(
        label='Email Principal',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'contacto@empresa.com'
        })
    )
    
    email_facturacion = forms.EmailField(
        label='Email de Facturación',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'facturacion@empresa.com (opcional)'
        })
    )
    
    sitio_web = forms.URLField(
        label='Sitio Web',
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://www.empresa.com (opcional)'
        })
    )
    
    horario_atencion = forms.CharField(
        label='Horario de Atención',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Ej: Lunes a Viernes 8:00 AM - 5:00 PM'
        })
    )
    
    # ===== INFORMACIÓN BANCARIA =====
    banco = forms.CharField(
        label='Banco',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Bancolombia'
        })
    )
    
    tipo_cuenta = forms.ChoiceField(
        label='Tipo de Cuenta',
        choices=[('', '-- Seleccione --')] + list(Proveedor._meta.get_field('tipo_cuenta').choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    numero_cuenta = forms.CharField(
        label='Número de Cuenta',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de cuenta bancaria'
        })
    )
    
    titular_cuenta = forms.CharField(
        label='Titular de la Cuenta',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del titular'
        })
    )
    
    # ===== CONDICIONES COMERCIALES =====
    plazo_entrega_dias = forms.IntegerField(
        label='Plazo de Entrega (días)',
        initial=0,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0'
        })
    )
    
    tiempo_credito_dias = forms.IntegerField(
        label='Tiempo de Crédito (días)',
        initial=0,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0'
        }),
        help_text='Días de crédito que ofrece el proveedor'
    )
    
    descuento_pronto_pago = forms.DecimalField(
        label='Descuento Pronto Pago (%)',
        initial=0,
        min_value=0,
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'step': '0.01'
        })
    )
    
    monto_minimo_pedido = forms.DecimalField(
        label='Monto Mínimo de Pedido',
        required=False,
        min_value=0,
        max_digits=15,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'step': '0.01',
            'placeholder': 'Valor mínimo de compra (opcional)'
        })
    )
    
    acepta_credito = forms.BooleanField(
        label='¿Acepta ventas a crédito?',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    metodos_pago_aceptados = forms.CharField(
        label='Métodos de Pago Aceptados',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Ej: Efectivo, Transferencia bancaria, Cheque'
        })
    )
    
    # ===== OBSERVACIONES =====
    observaciones_generales = forms.CharField(
        label='Observaciones Generales',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Notas adicionales sobre el proveedor...'
        })
    )
    
    class Meta:
        model = Proveedor
        fields = [
            # Identificación
            'razon_social', 'nombre_comercial', 'tipo_documento', 'numero_documento',
            'digito_verificacion', 'tipo_proveedor', 'categoria_principal', 'estado',
            # Legal y Tributaria
            'regimen_tributario', 'responsabilidad_fiscal', 'actividad_economica',
            'codigo_ciiu', 'pais_origen',
            # Contacto
            'direccion_principal', 'ciudad', 'departamento', 'pais', 'codigo_postal',
            'telefono_principal', 'telefono_secundario', 'email_principal',
            'email_facturacion', 'sitio_web', 'horario_atencion',
            # Bancaria
            'banco', 'tipo_cuenta', 'numero_cuenta', 'titular_cuenta',
            # Comerciales
            'plazo_entrega_dias', 'tiempo_credito_dias', 'descuento_pronto_pago',
            'monto_minimo_pedido', 'acepta_credito', 'metodos_pago_aceptados',
            # Observaciones
            'observaciones_generales'
        ]
    
    def clean_numero_documento(self):
        """Validar que el documento no esté duplicado"""
        numero_documento = self.cleaned_data.get('numero_documento')
        
        # Si estamos editando, excluir el proveedor actual
        queryset = Proveedor.objects.filter(numero_documento=numero_documento)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise forms.ValidationError(
                f'Ya existe un proveedor con el documento {numero_documento}'
            )
        
        return numero_documento
    
    def clean(self):
        """Validaciones personalizadas"""
        cleaned_data = super().clean()
        
        # Si marcó que acepta crédito, validar que tenga tiempo de crédito
        acepta_credito = cleaned_data.get('acepta_credito')
        tiempo_credito = cleaned_data.get('tiempo_credito_dias')
        
        if acepta_credito and tiempo_credito == 0:
            self.add_error('tiempo_credito_dias', 
                          'Si acepta crédito, debe indicar los días de crédito')
        
        return cleaned_data


# =====================================================
# FORMULARIO DE CONTACTOS - FASE 3
# =====================================================

from .models import ContactoProveedor


class ContactoProveedorForm(forms.ModelForm):
    """
    Formulario para crear/editar contactos de proveedores
    """
    
    nombre_completo = forms.CharField(
        label='Nombre Completo',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre completo del contacto'
        })
    )
    
    cargo = forms.CharField(
        label='Cargo',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Gerente de Ventas'
        })
    )
    
    departamento = forms.CharField(
        label='Departamento',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Ventas, Producción (opcional)'
        })
    )
    
    area_responsabilidad = forms.ChoiceField(
        label='Área de Responsabilidad',
        choices=ContactoProveedor._meta.get_field('area_responsabilidad').choices,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    telefono_directo = forms.CharField(
        label='Teléfono Directo / Extensión',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Extensión o línea directa (opcional)'
        })
    )
    
    telefono_celular = forms.CharField(
        label='Teléfono Celular',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de celular'
        })
    )
    
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@ejemplo.com'
        })
    )
    
    es_contacto_principal = forms.BooleanField(
        label='¿Es el contacto principal?',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        help_text='Solo puede haber un contacto principal por proveedor'
    )
    
    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Notas adicionales sobre el contacto...'
        })
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
        model = ContactoProveedor
        fields = [
            'nombre_completo',
            'cargo',
            'departamento',
            'area_responsabilidad',
            'telefono_directo',
            'telefono_celular',
            'email',
            'es_contacto_principal',
            'observaciones',
            'activo'
        ]
    
    def __init__(self, *args, **kwargs):
        self.proveedor = kwargs.pop('proveedor', None)
        super().__init__(*args, **kwargs)
    
    def clean_es_contacto_principal(self):
        """
        Validar que no haya conflictos con otros contactos principales
        """
        es_principal = self.cleaned_data.get('es_contacto_principal')
        
        if es_principal and self.proveedor:
            # Verificar si ya existe otro contacto principal
            existe_principal = ContactoProveedor.objects.filter(
                id_proveedor=self.proveedor,
                es_contacto_principal=True
            )
            
            # Si estamos editando, excluir el contacto actual
            if self.instance.pk:
                existe_principal = existe_principal.exclude(pk=self.instance.pk)
            
            if existe_principal.exists():
                # No es error, solo advertir que se cambiará automáticamente
                pass
        
        return es_principal
