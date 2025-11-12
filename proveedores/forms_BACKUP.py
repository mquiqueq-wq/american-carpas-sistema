"""
Formularios para el módulo de gestión de proveedores
American Carpas 1 SAS
Incluye: Catálogos, Proveedores, Contactos, Documentos y Productos/Servicios
"""

from django import forms
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
# FORMULARIOS DE CATÁLOGOS - FASE 1
# =====================================================

class TipoProveedorForm(forms.ModelForm):
    """Formulario para tipos de proveedores"""
    
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
            'placeholder': 'Descripción del tipo de proveedor...'
        })
    )
    
    icono = forms.CharField(
        label='Icono (clase Bootstrap Icons)',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: bi-building, bi-truck, bi-shop'
        }),
        help_text='Clase de icono de Bootstrap Icons'
    )

    activo = forms.BooleanField(
        label='Activo',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = TipoProveedor
        fields = ['nombre_tipo', 'descripcion', 'icono', 'activo']


class CategoriaProveedorForm(forms.ModelForm):
    """Formulario para categorías de proveedores"""
    
    nombre_categoria = forms.CharField(
        label='Nombre de la Categoría',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Textiles, Metalmecánica, Servicios'
        })
    )
    
    descripcion = forms.CharField(
        label='Descripción',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descripción de la categoría...'
        })
    )
    
    categoria_padre = forms.ModelChoiceField(
        label='Categoría Padre',
        queryset=CategoriaProveedor.objects.filter(activo=True),
        required=False,
        empty_label='-- Sin categoría padre (es categoría principal) --',
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Selecciona una categoría superior si esta es una subcategoría'
    )
    
    icono = forms.CharField(
        label='Icono (clase Bootstrap Icons)',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: bi-box, bi-tools'
        }),
        help_text='Clase de icono de Bootstrap Icons'
    )
    
    color = forms.CharField(
        label='Color',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'color'
        }),
        help_text='Color para identificar la categoría'
    )
    
    activo = forms.BooleanField(
        label='Activo',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = CategoriaProveedor
        fields = ['nombre_categoria', 'descripcion', 'categoria_padre', 'icono', 'color', 'activo']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['categoria_padre'].queryset = CategoriaProveedor.objects.filter(
                activo=True
            ).exclude(pk=self.instance.pk)


class TipoDocumentoProveedorForm(forms.ModelForm):
    """Formulario para tipos de documentos"""
    
    nombre_tipo_documento = forms.CharField(
        label='Nombre del Tipo de Documento',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: RUT, Cámara de Comercio, Estados Financieros'
        })
    )
    
    descripcion = forms.CharField(
        label='Descripción',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descripción del tipo de documento...'
        })
    )
    
    icono = forms.CharField(
        label='Icono (clase Bootstrap Icons)',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: bi-file-text, bi-file-earmark, bi-clipboard'
        }),
        help_text='Clase de icono de Bootstrap Icons'
    )

    obligatorio = forms.BooleanField(
        label='Documento Obligatorio',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Marcar si este documento es requerido para todos los proveedores'
    )
    
    requiere_vigencia = forms.BooleanField(
        label='Requiere Control de Vigencia',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Marcar si el documento tiene fecha de vencimiento'
    )
    
    dias_alerta_vencimiento = forms.IntegerField(
        label='Días de Alerta antes del Vencimiento',
        initial=30,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1'
        }),
        help_text='Días antes del vencimiento para enviar alertas'
    )
    
    activo = forms.BooleanField(
        label='Activo',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = TipoDocumentoProveedor
        fields = [
            'nombre_tipo_documento',
            'descripcion',
            'icono',
            'obligatorio',
            'requiere_vigencia',
            'dias_alerta_vencimiento',
            'activo'
        ]


# =====================================================
# FORMULARIO DE PROVEEDOR - FASE 2
# =====================================================

class ProveedorForm(forms.ModelForm):
    """Formulario para crear/editar proveedores"""
    
    # Identificación Básica
    tipo_persona = forms.ChoiceField(
        label='Tipo de Persona',
        choices=Proveedor._meta.get_field('tipo_persona').choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    razon_social = forms.CharField(
        label='Razón Social',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre legal completo del proveedor'
        })
    )
    
    nombre_comercial = forms.CharField(
        label='Nombre Comercial',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre comercial (opcional)'
        })
    )
    
    tipo_documento = forms.ChoiceField(
        label='Tipo de Documento',
        choices=Proveedor._meta.get_field('tipo_documento').choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    numero_documento = forms.CharField(
        label='Número de Documento',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'NIT, CC, CE o Pasaporte'
        })
    )
    
    digito_verificacion = forms.CharField(
        label='Dígito de Verificación',
        max_length=1,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'DV (solo para NIT)'
        })
    )
    
    # Clasificación
    tipo_proveedor = forms.ModelChoiceField(
        label='Tipo de Proveedor',
        queryset=TipoProveedor.objects.filter(activo=True),
        empty_label='-- Seleccione un tipo --',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    categoria_principal = forms.ModelChoiceField(
        label='Categoría Principal',
        queryset=CategoriaProveedor.objects.filter(activo=True),
        empty_label='-- Seleccione una categoría --',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Información Legal y Tributaria
    regimen_tributario = forms.CharField(
        label='Régimen Tributario',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Régimen Común, Simplificado'
        })
    )
    
    # Responsabilidad Fiscal (Select único)
    responsabilidad_fiscal = forms.ChoiceField(
        label='Responsabilidad Fiscal',
        choices=Proveedor._meta.get_field('responsabilidad_fiscal').choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Seleccione la responsabilidad fiscal del proveedor'
    )

    # NUEVOS: Campos adicionales legales
    pais_origen = forms.CharField(
        label='País de Origen',
        max_length=100,
        initial='Colombia',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'País donde está constituida la empresa'
        })
    )
    actividad_economica = forms.CharField(
        label='Actividad Económica',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Descripción de la actividad económica'
        })
    )
    
    codigo_ciiu = forms.CharField(
        label='Código CIIU',
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 4711'
        })
    )
   
    
    # Información de Contacto
    pais = forms.CharField(
        label='País',
        max_length=100,
        initial='Colombia',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    departamento = forms.CharField(
        label='Departamento/Estado',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Antioquia'
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
    
    direccion = forms.CharField(
        label='Dirección',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dirección completa'
        })
    )
    
    codigo_postal = forms.CharField(
        label='Código Postal',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '050001'
        })
    )
    
    telefono_principal = forms.CharField(
        label='Teléfono Principal',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+57 300 123 4567'
        })
    )
    
    telefono_secundario = forms.CharField(
        label='Teléfono Secundario',
        max_length=50,
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
            'placeholder': 'contacto@proveedor.com'
        })
    )
    
    email_secundario = forms.EmailField(
        label='Email Secundario',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional'
        })
    )
    email_facturacion = forms.EmailField(
        label='Email de Facturación',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email para facturación electrónica'
        })
    )
    
    horario_atencion = forms.CharField(
        label='Horario de Atención',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Lunes a Viernes 8:00 AM - 5:00 PM'
        })
    )

    sitio_web = forms.URLField(
        label='Sitio Web',
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://www.ejemplo.com'
        })
    )
    
    # Información Bancaria
    banco = forms.CharField(
        label='Banco',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del banco'
        })
    )
    
    tipo_cuenta = forms.CharField(
        label='Tipo de Cuenta',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ahorros, Corriente'
        })
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
            'placeholder': 'Nombre del titular de la cuenta'
        })
    )
    
    # Información Comercial
    tiempo_entrega_promedio = forms.IntegerField(
        label='Tiempo de Entrega Promedio (días)',
        initial=0,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0'
        })
    )
    
    condiciones_pago = forms.CharField(
        label='Condiciones de Pago',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 30 días, Contado'
        })
    )
    
    monto_minimo_pedido = forms.DecimalField(
        label='Monto Mínimo de Pedido',
        initial=0,
        min_value=0,
        max_digits=15,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'step': '0.01'
        })
    )
    
    descuento_pronto_pago = forms.DecimalField(
        label='Descuento por Pronto Pago (%)',
        initial=0,
        min_value=0,
        max_value=100,
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '100',
            'step': '0.01'
        })
    )
    acepta_credito = forms.BooleanField(
        label='Acepta Crédito',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='¿El proveedor acepta ventas a crédito?'
    )
    
    metodos_pago_aceptados = forms.CharField(
        label='Métodos de Pago Aceptados',
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Efectivo, Transferencia, Cheque, Tarjeta de Crédito'
        })
    )
    
    calificacion = forms.DecimalField(
        label='Calificación (0.00 - 5.00)',
        initial=0,
        min_value=0,
        max_value=5,
        max_digits=3,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '5',
            'step': '0.01'
        })
    )
    
    # Observaciones
    notas_internas = forms.CharField(
        label='Notas Internas',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Notas privadas, no visibles para el proveedor...'
        })
    )
    
    observaciones = forms.CharField(
        label='Observaciones Generales',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Observaciones generales...'
        })
    )
    
    # Estado
    estado = forms.ChoiceField(
        label='Estado',
        choices=Proveedor._meta.get_field('estado').choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = Proveedor
        fields = [
            # Identificación
            'tipo_persona', 'razon_social', 'nombre_comercial', 'tipo_documento',
            'numero_documento', 'digito_verificacion', 'tipo_proveedor',
            'categoria_principal', 'estado',
            # Legal y Tributaria
            'regimen_tributario', 'responsabilidad_fiscal', 'pais_origen',
            'actividad_economica', 'codigo_ciiu',
            # Contacto
            'pais', 'departamento', 'ciudad', 'direccion', 'codigo_postal',
            'telefono_principal', 'telefono_secundario', 
            'email_principal', 'email_secundario', 'email_facturacion',
            'sitio_web', 'horario_atencion',
            # Bancaria
            'banco', 'tipo_cuenta', 'numero_cuenta', 'titular_cuenta',
            # Comercial
            'tiempo_entrega_promedio', 'condiciones_pago', 'monto_minimo_pedido',
            'descuento_pronto_pago', 'acepta_credito', 'metodos_pago_aceptados',
            'calificacion',
            # Observaciones
            'notas_internas', 'observaciones'
        ]
    
    def clean_numero_documento(self):
        """Validar que el número de documento sea único"""
        numero_documento = self.cleaned_data.get('numero_documento')
        
        # Verificar duplicados
        existe = Proveedor.objects.filter(numero_documento=numero_documento)
        
        # Si estamos editando, excluir el proveedor actual
        if self.instance.pk:
            existe = existe.exclude(pk=self.instance.pk)
        
        if existe.exists():
            raise forms.ValidationError(
                f'Ya existe un proveedor con el documento {numero_documento}'
            )
        
        return numero_documento


# =====================================================
# FORMULARIO DE CONTACTOS - FASE 3
# =====================================================

class ContactoProveedorForm(forms.ModelForm):
    """Formulario para contactos de proveedores"""
    
    id_proveedor = forms.ModelChoiceField(
        label='Proveedor',
        queryset=Proveedor.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        disabled=True
    )
    
    nombres = forms.CharField(
        label='Nombres',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombres del contacto'
        })
    )
    
    apellidos = forms.CharField(
        label='Apellidos',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellidos del contacto'
        })
    )
    
    cargo = forms.CharField(
        label='Cargo',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Gerente Comercial, Vendedor'
        })
    )
    
    area_responsabilidad = forms.ChoiceField(
        label='Área de Responsabilidad',
        choices=[
            ('COMERCIAL', 'Comercial'),
            ('TECNICA', 'Técnica'),
            ('FINANCIERA', 'Financiera'),
            ('LOGISTICA', 'Logística'),
            ('CALIDAD', 'Calidad'),
            ('ADMINISTRATIVA', 'Administrativa'),
            ('OTRA', 'Otra'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    telefono_fijo = forms.CharField(
        label='Teléfono Fijo',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional'
        })
    )
    
    telefono_movil = forms.CharField(
        label='Teléfono Móvil',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+57 300 123 4567'
        })
    )
    
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'contacto@ejemplo.com'
        })
    )
    
    es_contacto_principal = forms.BooleanField(
        label='Contacto Principal',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Solo puede haber un contacto principal por proveedor'
    )
    
    activo = forms.BooleanField(
        label='Activo',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Notas adicionales sobre el contacto...'
        })
    )
    
    class Meta:
        model = ContactoProveedor
        fields = [
            'id_proveedor', 'nombres', 'apellidos', 'cargo', 'area_responsabilidad',
            'telefono_fijo', 'telefono_movil', 'email',
            'es_contacto_principal', 'activo', 'observaciones'
        ]


# =====================================================
# FORMULARIO DE DOCUMENTOS - FASE 4
# =====================================================

class DocumentoProveedorForm(forms.ModelForm):
    """Formulario para cargar/editar documentos de proveedores"""
    
    id_tipo_documento = forms.ModelChoiceField(
        label='Tipo de Documento',
        queryset=TipoDocumentoProveedor.objects.filter(activo=True),
        empty_label='-- Seleccione un tipo --',
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Tipo de documento que está cargando'
    )
    
    archivo = forms.FileField(
        label='Archivo',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.jpg,.jpeg,.png,.doc,.docx'
        }),
        help_text='Formatos permitidos: PDF, JPG, PNG, DOC, DOCX (Máx. 10MB)'
    )
    
    numero_documento = forms.CharField(
        label='Número de Documento',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de folio, certificado, etc. (opcional)'
        })
    )
    
    fecha_emision = forms.DateField(
        label='Fecha de Emisión',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    fecha_vencimiento = forms.DateField(
        label='Fecha de Vencimiento',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        help_text='Dejar vacío si el documento no vence'
    )
    
    entidad_emisora = forms.CharField(
        label='Entidad Emisora',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Cámara de Comercio, DIAN, etc.'
        })
    )
    
    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Notas adicionales sobre el documento...'
        })
    )
    
    class Meta:
        model = DocumentoProveedor
        fields = [
            'id_tipo_documento', 'archivo', 'numero_documento',
            'fecha_emision', 'fecha_vencimiento', 'entidad_emisora',
            'observaciones'
        ]
    
    def __init__(self, *args, **kwargs):
        self.proveedor = kwargs.pop('proveedor', None)
        super().__init__(*args, **kwargs)
        
        if self.instance.pk:
            self.fields['archivo'].required = False
            self.fields['archivo'].help_text = 'Dejar vacío para mantener el archivo actual'
    
    def clean_fecha_vencimiento(self):
        """Validar que la fecha de vencimiento sea posterior a la emisión"""
        fecha_emision = self.cleaned_data.get('fecha_emision')
        fecha_vencimiento = self.cleaned_data.get('fecha_vencimiento')
        
        if fecha_vencimiento and fecha_emision:
            if fecha_vencimiento <= fecha_emision:
                raise forms.ValidationError(
                    'La fecha de vencimiento debe ser posterior a la fecha de emisión'
                )
        
        return fecha_vencimiento
    
    def clean_archivo(self):
        """Validar el archivo cargado"""
        archivo = self.cleaned_data.get('archivo')
        
        if not archivo and self.instance.pk:
            return archivo
        
        if archivo:
            if archivo.size > 10 * 1024 * 1024:
                raise forms.ValidationError(
                    'El archivo es demasiado grande. Tamaño máximo: 10MB'
                )
            
            import os
            ext = os.path.splitext(archivo.name)[1].lower()
            extensiones_permitidas = ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx']
            
            if ext not in extensiones_permitidas:
                raise forms.ValidationError(
                    f'Formato no permitido. Use: {", ".join(extensiones_permitidas)}'
                )
        
        return archivo
    
    def clean(self):
        """Validar que no exista ya este tipo de documento para el proveedor"""
        cleaned_data = super().clean()
        tipo_documento = cleaned_data.get('id_tipo_documento')
        
        if tipo_documento and self.proveedor:
            existe = DocumentoProveedor.objects.filter(
                id_proveedor=self.proveedor,
                id_tipo_documento=tipo_documento
            )
            
            if self.instance.pk:
                existe = existe.exclude(pk=self.instance.pk)
            
            if existe.exists():
                self.add_error('id_tipo_documento',
                              f'Ya existe un documento de tipo "{tipo_documento.nombre_tipo_documento}" para este proveedor')
        
        return cleaned_data


# =====================================================
# FORMULARIO DE PRODUCTOS/SERVICIOS - FASE 5
# =====================================================

class ProductoServicioProveedorForm(forms.ModelForm):
    """Formulario para crear/editar productos y servicios de proveedores"""
    
    tipo = forms.ChoiceField(
        label='Tipo',
        choices=ProductoServicioProveedor._meta.get_field('tipo').choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    nombre = forms.CharField(
        label='Nombre del Producto/Servicio',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre descriptivo del producto o servicio'
        })
    )
    
    descripcion = forms.CharField(
        label='Descripción',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descripción detallada...'
        })
    )
    
    sku_codigo = forms.CharField(
        label='SKU / Código',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Código o referencia del proveedor'
        })
    )
    
    marca = forms.CharField(
        label='Marca',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Marca del producto (si aplica)'
        })
    )
    
    unidad_medida = forms.ChoiceField(
        label='Unidad de Medida',
        choices=ProductoServicioProveedor._meta.get_field('unidad_medida').choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    precio_unitario = forms.DecimalField(
        label='Precio Unitario',
        min_value=0,
        max_digits=15,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'step': '0.01',
            'placeholder': '0.00'
        })
    )
    
    moneda = forms.ChoiceField(
        label='Moneda',
        choices=ProductoServicioProveedor._meta.get_field('moneda').choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    precio_especial = forms.DecimalField(
        label='Precio Especial',
        required=False,
        min_value=0,
        max_digits=15,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'step': '0.01',
            'placeholder': 'Precio con descuento (opcional)'
        }),
        help_text='Precio promocional o con descuento'
    )
    
    descuento_porcentaje = forms.DecimalField(
        label='Descuento (%)',
        initial=0,
        min_value=0,
        max_value=100,
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '100',
            'step': '0.01'
        })
    )
    
    cantidad_minima = forms.IntegerField(
        label='Cantidad Mínima de Compra',
        initial=1,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1'
        })
    )
    
    tiempo_entrega_dias = forms.IntegerField(
        label='Tiempo de Entrega (días)',
        initial=0,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0'
        })
    )
    
    disponible = forms.BooleanField(
        label='Disponible para compra',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    stock_disponible = forms.IntegerField(
        label='Stock Disponible',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'placeholder': 'Opcional'
        }),
        help_text='Cantidad en inventario (opcional)'
    )
    
    especificaciones_tecnicas = forms.CharField(
        label='Especificaciones Técnicas',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Dimensiones, materiales, características técnicas...'
        })
    )
    
    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Notas adicionales...'
        })
    )
    
    activo = forms.BooleanField(
        label='Activo en catálogo',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = ProductoServicioProveedor
        fields = [
            'tipo', 'nombre', 'descripcion', 'sku_codigo', 'marca',
            'unidad_medida', 'precio_unitario', 'moneda', 'precio_especial',
            'descuento_porcentaje', 'cantidad_minima', 'tiempo_entrega_dias',
            'disponible', 'stock_disponible', 'especificaciones_tecnicas',
            'observaciones', 'activo'
        ]
    
    def __init__(self, *args, **kwargs):
        self.proveedor = kwargs.pop('proveedor', None)
        super().__init__(*args, **kwargs)
    
    def clean_precio_especial(self):
        """Validar que el precio especial sea menor al precio unitario"""
        precio_unitario = self.cleaned_data.get('precio_unitario')
        precio_especial = self.cleaned_data.get('precio_especial')
        
        if precio_especial and precio_unitario:
            if precio_especial >= precio_unitario:
                raise forms.ValidationError(
                    'El precio especial debe ser menor al precio unitario'
                )
        
        return precio_especial
    
    def clean_sku_codigo(self):
        """Validar que el SKU no esté duplicado para el mismo proveedor"""
        sku_codigo = self.cleaned_data.get('sku_codigo')
        
        if sku_codigo and self.proveedor:
            existe = ProductoServicioProveedor.objects.filter(
                id_proveedor=self.proveedor,
                sku_codigo=sku_codigo
            )
            
            if self.instance.pk:
                existe = existe.exclude(pk=self.instance.pk)
            
            if existe.exists():
                raise forms.ValidationError(
                    f'Ya existe un producto con el código "{sku_codigo}" para este proveedor'
                )
        
        return sku_codigo
    
    def save(self, commit=True):
        """Guardar y actualizar fecha de última actualización de precio si cambió"""
        from datetime import date
        
        producto = super().save(commit=False)
        
        if self.instance.pk:
            if 'precio_unitario' in self.changed_data:
                producto.fecha_ultima_actualizacion_precio = date.today()
        else:
            producto.fecha_ultima_actualizacion_precio = date.today()
        
        if commit:
            producto.save()
        
        return producto