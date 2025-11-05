from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta

from .models import (
    TrabajadorPersonal, TrabajadorLaboral, TrabajadorAfiliaciones,
    TrabajadorDotacion, TrabajadorCurso, TrabajadorRol, TipoCurso, TipoDotacion, TipoDocumento, TrabajadorDocumento
)

# Widgets comunes
TEXT_INPUT = forms.TextInput(attrs={"class": "form-control"})
SELECT = forms.Select(attrs={"class": "form-select"})
DATE_INPUT = forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"})
DATETIME_INPUT = forms.DateTimeInput(format="%Y-%m-%dT%H:%M", attrs={"type": "datetime-local", "class": "form-control"})
NUMBER_INPUT = forms.NumberInput(attrs={"class": "form-control"})
EMAIL_INPUT = forms.EmailInput(attrs={"class": "form-control"})
TEXTAREA = forms.Textarea(attrs={"class": "form-control", "rows": 3})


class TrabajadorDotacionForm(forms.ModelForm):
    """
    Form para crear/editar dotaciones.
    Maneja:
    - Población dinámica de 'talla' tanto en GET como en POST.
    - Cálculo y seteo de 'fecha_vencimiento'.
    - Campo 'estado' incluido como en el modelo.
    """

    tipo_dotacion_catalogo = forms.ModelChoiceField(
        queryset=TipoDotacion.objects.filter(activo=True),
        required=True,
        label='Tipo de Dotación',
        empty_label='-- Seleccione un tipo --',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_tipo_dotacion_catalogo',
        })
    )

    talla = forms.ChoiceField(
        choices=[('', '-- Seleccione primero un tipo --')],
        required=False,
        label='Talla',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_talla'
        })
    )

    cantidad = forms.IntegerField(
        label='Cantidad',
        initial=1,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'value': '1'
        })
    )

    fecha_entrega = forms.DateField(
        label='Fecha de Entrega',
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={'type': 'date', 'class': 'form-control', 'id': 'id_fecha_entrega'}
        )
    )
    
    fecha_vencimiento = forms.DateField(
        label='Fecha de Vencimiento',
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'readonly': 'readonly',
            'id': 'id_fecha_vencimiento',
        }),
        help_text='Se calcula automáticamente'
    )

    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Observaciones adicionales...'
        })
    )

    class Meta:
        model = TrabajadorDotacion
        fields = [
            'tipo_dotacion_catalogo',
            'talla',
            'cantidad',
            'fecha_entrega',
            'fecha_vencimiento',
            'observaciones',
            'estado',
        ]
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select', 'id': 'id_estado'}),
        }
        labels = {
            'estado': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # POST: poblar choices de talla a partir del tipo enviado
        tipo_id_post = None
        if self.data and self.data.get('tipo_dotacion_catalogo'):
            try:
                tipo_id_post = int(self.data.get('tipo_dotacion_catalogo'))
            except (TypeError, ValueError):
                tipo_id_post = None

        if tipo_id_post:
            tipo = TipoDotacion.objects.filter(pk=tipo_id_post, activo=True).first()
            if tipo:
                if tipo.requiere_talla:
                    tallas_lista = tipo.get_tallas_lista()
                    self.fields['talla'].choices = [('', '-- Seleccione --')] + [(t, t) for t in tallas_lista]
                    self.fields['talla'].required = True
                else:
                    self.fields['talla'].choices = [('N/A', 'No aplica')]
                    self.fields['talla'].required = False
            else:
                self.fields['talla'].choices = [('', '-- Seleccione primero un tipo --')]
                self.fields['talla'].required = False
            return

        # Edición con instancia
        if self.instance and self.instance.pk and self.instance.tipo_dotacion_catalogo:
            tipo = self.instance.tipo_dotacion_catalogo
            if tipo.requiere_talla and tipo.tallas_disponibles:
                tallas_lista = tipo.get_tallas_lista()
                self.fields['talla'].choices = [('', '-- Seleccione --')] + [(t, t) for t in tallas_lista]
                self.fields['talla'].required = True
            else:
                self.fields['talla'].choices = [('N/A', 'No aplica')]
                self.fields['talla'].required = False
        else:
            # Crear sin selección previa
            self.fields['talla'].choices = [('', '-- Seleccione primero un tipo --')]
            self.fields['talla'].required = False

    def clean(self):
        cleaned_data = super().clean()
        tipo_catalogo = cleaned_data.get('tipo_dotacion_catalogo')
        talla = cleaned_data.get('talla')
        fecha_entrega = cleaned_data.get('fecha_entrega')

        if not tipo_catalogo:
            raise ValidationError('Debe seleccionar un tipo de dotación.')

        if tipo_catalogo.requiere_talla:
            if not talla:
                raise ValidationError({
                    'talla': f'Este tipo requiere talla. Disponibles: {tipo_catalogo.tallas_disponibles or "N/A"}'
                })
            tallas_validas = tipo_catalogo.get_tallas_lista()
            if tallas_validas and talla not in tallas_validas:
                raise ValidationError({
                    'talla': f'Talla "{talla}" no válida. Disponibles: {", ".join(tallas_validas)}'
                })
        else:
            cleaned_data['talla'] = 'N/A'

        # Calcular fecha de vencimiento
        if tipo_catalogo and fecha_entrega:
            cleaned_data['fecha_vencimiento'] = fecha_entrega + timedelta(days=tipo_catalogo.vida_util_dias)

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Sincronizar nombre legible
        if instance.tipo_dotacion_catalogo:
            instance.tipo_dotacion = instance.tipo_dotacion_catalogo.nombre_tipo_dotacion

        # Estado por defecto solo si viene vacío
        if not instance.estado:
            instance.estado = 'ACTIVO'

        if commit:
            instance.save()
        return instance


class TipoCursoForm(forms.ModelForm):
    class Meta:
        model = TipoCurso
        fields = [
            'nombre_tipo_curso',
            'vigencia_dias',
            'dias_alerta_anticipada',
            'requiere_renovacion',
            'normativa_referencia',
            'descripcion',
            'activo'
        ]
        widgets = {
            'nombre_tipo_curso': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Trabajo en Alturas - Avanzado'
            }),
            'vigencia_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Días de vigencia (ej: 365)',
                'min': 1
            }),
            'dias_alerta_anticipada': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '30',
                'min': 1
            }),
            'requiere_renovacion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'normativa_referencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Resolución 1409 de 2012'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción detallada del curso'
            }),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre_tipo_curso': 'Nombre del Tipo de Curso',
            'vigencia_dias': 'Vigencia (días)',
            'dias_alerta_anticipada': 'Días para alerta anticipada',
            'requiere_renovacion': '¿Requiere renovación?',
            'normativa_referencia': 'Normativa de referencia',
            'descripcion': 'Descripción',
            'activo': 'Activo'
        }


class TipoDotacionForm(forms.ModelForm):
    class Meta:
        model = TipoDotacion
        fields = [
            'nombre_tipo_dotacion',
            'vida_util_dias',
            'requiere_talla',
            'tallas_disponibles',
            'normativa_referencia',
            'descripcion',
            'activo'
        ]
        widgets = {
            'nombre_tipo_dotacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Casco de Seguridad'
            }),
            'vida_util_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Días de vida útil (ej: 365)',
                'min': 1
            }),
            'requiere_talla': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tallas_disponibles': forms.TextInput(attrs={
                'placeholder': 'Ej: S,M,L,XL o 35,36,37,38...',
                'class': 'form-control'
            }),
            'normativa_referencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Resolución 2400 de 1979'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del elemento'
            }),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre_tipo_dotacion': 'Nombre del Tipo de Dotación',
            'vida_util_dias': 'Vida útil (días)',
            'requiere_talla': '¿Requiere talla?',
            'tallas_disponibles': 'Tallas Disponibles',
            'normativa_referencia': 'Normativa de referencia',
            'descripcion': 'Descripción',
            'activo': 'Activo'
        }


class TrabajadorCursoForm(forms.ModelForm):
    """
    Form para crear/editar cursos de trabajadores.
    Maneja:
    - Selección de tipo de curso activo (obligatorio).
    - Cálculo de fecha de vencimiento (en el modelo, pero se puede mostrar en el template).
    - Filtrado de "es_renovacion_de" por trabajador.
    """

    tipo_curso = forms.ModelChoiceField(
        queryset=TipoCurso.objects.filter(activo=True),
        required=True,
        label='Tipo de Curso (Obligatorio)',
        empty_label='-- Seleccione un tipo --',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_tipo_curso'
        })
    )

    nombre_curso = forms.CharField(
        label='Nombre del Curso',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre completo del curso'
        })
    )

    institucion = forms.CharField(
        label='Institución',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Institución que dictó el curso'
        })
    )

    fecha_inicio_curso = forms.DateField(
        label='Fecha de Inicio',
        required=True,
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'id_fecha_inicio_curso'
            }
        )
    )

    fecha_fin_curso = forms.DateField(
        label='Fecha de Finalización',
        required=False,
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'id_fecha_fin_curso'
            }
        )
    )

    numero_certificado = forms.CharField(
        label='Número de Certificado',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número del certificado'
        })
    )

    certificado_url = forms.URLField(
        label='URL del Certificado',
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'URL del certificado (opcional)'
        })
    )

    es_renovacion_de = forms.ModelChoiceField(
        queryset=TrabajadorCurso.objects.none(),
        required=False,
        label='Es renovación de (opcional)',
        empty_label='-- No es renovación --',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_es_renovacion_de'
        })
    )

    class Meta:
        model = TrabajadorCurso
        fields = [
            'tipo_curso',
            'nombre_curso',
            'institucion',
            'fecha_inicio_curso',
            'fecha_fin_curso',
            'numero_certificado',
            'certificado_url',
            'es_renovacion_de'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Solo tipos activos
        self.fields['tipo_curso'].required = True
        self.fields['tipo_curso'].queryset = TipoCurso.objects.filter(activo=True)

        # Poblamos "es_renovacion_de" solo si tenemos instancia con trabajador
        qs = TrabajadorCurso.objects.none()
        if self.instance and getattr(self.instance, 'id_trabajador_id', None):
            qs = TrabajadorCurso.objects.filter(
                id_trabajador=self.instance.id_trabajador
            ).exclude(
                id_curso=self.instance.pk if self.instance.pk else None
            )
        # Si no hay instance.id_trabajador (caso create), la vista lo asignará
        # y este queryset se repoblará en la vista
        self.fields['es_renovacion_de'].queryset = qs

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('fecha_inicio_curso')
        fin = cleaned_data.get('fecha_fin_curso')
        tipo_curso = cleaned_data.get('tipo_curso')
        nombre = cleaned_data.get('nombre_curso')

        # Validar coherencia de fechas
        if inicio and fin and fin < inicio:
            self.add_error(
                'fecha_fin_curso',
                'La fecha de finalización debe ser posterior o igual a la fecha de inicio.'
            )

        # Autollenar nombre_curso si está vacío y hay tipo seleccionado
        if not nombre and tipo_curso:
            cleaned_data['nombre_curso'] = tipo_curso.nombre_tipo_curso

        # Validar que tipo_curso esté seleccionado
        if not tipo_curso:
            raise ValidationError('Debe seleccionar un tipo de curso.')

        return cleaned_data


class TrabajadorPersonalForm(forms.ModelForm):
    class Meta:
        model = TrabajadorPersonal
        fields = [
            'tipo_documento','id_trabajador', 'nombres', 'apellidos', 'fecha_expedicion_doc', 'lugar_expedicion',
            'nacionalidad', 'fecha_nacimiento', 'lugar_nacimiento', 'genero', 'estado_civil',
            'direccion_residencia', 'ciudad_residencia', 'departamento_residencia',
            'telefono_celular', 'correo_personal', 'grupo_sanguineo_rh', 'nombres_padre', 'nombres_madre',
            'nombre_contacto_emergencia', 'numero_contacto_emergencia',
            'numero_hijos', 'cuenta_bancaria', 'tipo_cuenta', 'banco'
        ]
        widgets = {
            'tipo_documento': SELECT,
            'id_trabajador': forms.TextInput(attrs={"class": "form-control","placeholder": "Número de documento"}),
            'nombres': TEXT_INPUT,
            'apellidos': TEXT_INPUT,
            'fecha_expedicion_doc': DATE_INPUT,
            'lugar_expedicion': TEXT_INPUT,
            'nacionalidad': TEXT_INPUT,
            'fecha_nacimiento': DATE_INPUT,
            'lugar_nacimiento': TEXT_INPUT,
            'genero': SELECT,
            'estado_civil': SELECT,
            'direccion_residencia': TEXT_INPUT,
            'ciudad_residencia': TEXT_INPUT,
            'departamento_residencia': TEXT_INPUT,
            'telefono_celular': TEXT_INPUT,
            'correo_personal': EMAIL_INPUT,
            'grupo_sanguineo_rh': TEXT_INPUT,
            'nombres_padre': TEXT_INPUT,
            'nombres_madre': TEXT_INPUT,
            'nombre_contacto_emergencia': TEXT_INPUT,
            'numero_contacto_emergencia': TEXT_INPUT,
            'numero_hijos': NUMBER_INPUT,
            'cuenta_bancaria': TEXT_INPUT,
            'tipo_cuenta': SELECT,
            'banco': TEXT_INPUT,
        }

    def clean_telefono_celular(self):
        tel = self.cleaned_data.get('telefono_celular', '').strip()
        if len(tel) < 7:
            raise forms.ValidationError("El teléfono celular parece demasiado corto.")
        return tel

    def clean(self):
        cleaned = super().clean()
        fn = cleaned.get('fecha_nacimiento')
        fe = cleaned.get('fecha_expedicion_doc')
        if fn and fe and fe <= fn:
            self.add_error('fecha_expedicion_doc', "La fecha de expedición debe ser posterior a la fecha de nacimiento.")
        return cleaned


class TrabajadorLaboralForm(forms.ModelForm):
    class Meta:
        model = TrabajadorLaboral
        fields = [
            'id_trabajador', 'tipo_contrato', 'fecha_inicio_contrato', 'cargo', 'salario',
            'jornada_laboral', 'sede_trabajo', 'fecha_terminacion_contrato', 'motivo_terminacion'
        ]
        widgets = {
            'id_trabajador': SELECT,
            'tipo_contrato': SELECT,
            'fecha_inicio_contrato': DATE_INPUT,
            'cargo': TEXT_INPUT,
            'salario': NUMBER_INPUT,
            'jornada_laboral': SELECT,
            'sede_trabajo': TEXT_INPUT,
            'fecha_terminacion_contrato': DATE_INPUT,
            'motivo_terminacion': TEXT_INPUT,
        }

    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get('fecha_inicio_contrato')
        fin = cleaned.get('fecha_terminacion_contrato')
        if fin and inicio and fin <= inicio:
            self.add_error('fecha_terminacion_contrato', "La fecha de terminación debe ser posterior al inicio.")
        return cleaned


class TrabajadorAfiliacionesForm(forms.ModelForm):
    class Meta:
        model = TrabajadorAfiliaciones
        fields = [
            'id_trabajador',
            'eps_nombre', 'eps_numero_afiliacion',
            'fondo_pensiones_nombre', 'fondo_pensiones_numero_afiliacion',
            'arl_nombre', 'arl_numero_nombre',
            'caja_compensacion_nombre', 'caja_compensacion_numero_afiliacion',
        ]
        widgets = {
            'id_trabajador': SELECT,
            'eps_nombre': TEXT_INPUT,
            'eps_numero_afiliacion': TEXT_INPUT,
            'fondo_pensiones_nombre': TEXT_INPUT,
            'fondo_pensiones_numero_afiliacion': TEXT_INPUT,
            'arl_nombre': TEXT_INPUT,
            'arl_numero_nombre': TEXT_INPUT,
            'caja_compensacion_nombre': TEXT_INPUT,
            'caja_compensacion_numero_afiliacion': TEXT_INPUT,
        }


class TrabajadorRolForm(forms.ModelForm):
    class Meta:
        model = TrabajadorRol
        fields = ['id_trabajador', 'rol_sistema', 'estado_cuenta', 'password_hash', 'ultimo_inicio_sesion']
        widgets = {
            'id_trabajador': SELECT,
            'rol_sistema': TEXT_INPUT,
            'estado_cuenta': SELECT,
            'password_hash': TEXT_INPUT,
            'ultimo_inicio_sesion': DATETIME_INPUT,
        }
        labels = {
            'id_trabajador': 'Trabajador',
            'rol_sistema': 'Rol en el sistema',
            'estado_cuenta': 'Estado de la cuenta',
            'password_hash': 'Hash de contraseña',
            'ultimo_inicio_sesion': 'Último inicio de sesión',
        }
class TipoDocumentoForm(forms.ModelForm):
    """
    Formulario para crear/editar tipos de documentos en el catálogo.
    Permite configurar si es obligatorio, requiere vigencia, etc.
    """
    
    nombre_tipo_documento = forms.CharField(
        label='Nombre del Tipo de Documento',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Fotocopia Cédula, Certificado Curso, Afiliación EPS'
        }),
        help_text='Nombre descriptivo del tipo de documento'
    )
    
    descripcion = forms.CharField(
        label='Descripción',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descripción detallada del tipo de documento...'
        }),
        help_text='Descripción opcional del documento'
    )
    
    icono_bootstrap = forms.CharField(
        label='Icono Bootstrap',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'bi-file-earmark-text'
        }),
        help_text='Ej: bi-file-earmark-text, bi-card-checklist, bi-hospital'
    )
    
    orden_visualizacion = forms.IntegerField(
        label='Orden de Visualización',
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0'
        }),
        help_text='Número de orden (menor = aparece primero)'
    )

    class Meta:
        model = TipoDocumento
        fields = [
            'nombre_tipo_documento',
            'descripcion',
            'es_obligatorio',
            'requiere_vigencia',
            'icono_bootstrap',
            'orden_visualizacion',
            'activo'
        ]
        widgets = {
            'es_obligatorio': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_es_obligatorio'
            }),
            'requiere_vigencia': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_requiere_vigencia'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_activo'
            }),
        }
        labels = {
            'es_obligatorio': '¿Es obligatorio?',
            'requiere_vigencia': '¿Requiere control de vigencia?',
            'activo': 'Activo'
        }
        help_texts = {
            'es_obligatorio': 'Marca si este documento es obligatorio para todos los trabajadores',
            'requiere_vigencia': 'Marca si el documento tiene fecha de vencimiento',
            'activo': 'Solo los tipos activos están disponibles para asignar'
        }

    def clean_nombre_tipo_documento(self):
        """Validar que no exista otro tipo con el mismo nombre"""
        nombre = self.cleaned_data.get('nombre_tipo_documento')
        
        # Verificar duplicados (excepto la misma instancia en edición)
        qs = TipoDocumento.objects.filter(nombre_tipo_documento__iexact=nombre)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        
        if qs.exists():
            raise ValidationError(
                'Ya existe un tipo de documento con este nombre. '
                'Por favor, usa un nombre diferente.'
            )
        
        return nombre

    def clean_orden_visualizacion(self):
        """Validar que el orden sea un número positivo"""
        orden = self.cleaned_data.get('orden_visualizacion')
        if orden is not None and orden < 0:
            raise ValidationError('El orden debe ser un número positivo o cero.')
        return orden


class TrabajadorDocumentoForm(forms.ModelForm):
    """
    Formulario para agregar/editar documentos de un trabajador.
    Maneja la subida de archivos y control de vigencia opcional.
    """
    
    tipo_documento = forms.ModelChoiceField(
        queryset=TipoDocumento.objects.filter(activo=True).order_by('orden_visualizacion', 'nombre_tipo_documento'),
        required=True,
        label='Tipo de Documento',
        empty_label='-- Seleccione un tipo de documento --',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_tipo_documento'
        }),
        help_text='Seleccione el tipo de documento del catálogo'
    )
    
    archivo = forms.FileField(
        label='Archivo',
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'id': 'id_archivo',
            'accept': '.pdf,.jpg,.jpeg,.png,.doc,.docx,.xls,.xlsx'
        }),
        help_text='Formatos permitidos: PDF, Imágenes (JPG, PNG), Word, Excel. Tamaño máximo: 10 MB'
    )
    
    vigencia_desde = forms.DateField(
        label='Vigente desde',
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'id': 'id_vigencia_desde'
        }),
        help_text='Fecha de inicio de vigencia (opcional)'
    )
    
    vigencia_hasta = forms.DateField(
        label='Vigente hasta',
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'id': 'id_vigencia_hasta'
        }),
        help_text='Fecha de vencimiento del documento (solo si el tipo requiere vigencia)'
    )
    
    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Notas adicionales sobre el documento...'
        }),
        help_text='Observaciones opcionales sobre el documento'
    )

    class Meta:
        model = TrabajadorDocumento
        fields = [
            'tipo_documento',
            'archivo',
            'vigencia_desde',
            'vigencia_hasta',
            'observaciones'
        ]

    def __init__(self, *args, **kwargs):
        """
        Inicializar el formulario.
        En edición, el archivo no es obligatorio (ya existe uno)
        """
        super().__init__(*args, **kwargs)
        
        # Si estamos editando, hacer el archivo opcional
        if self.instance and self.instance.pk:
            self.fields['archivo'].required = False
            self.fields['archivo'].help_text = 'Deja vacío para mantener el archivo actual. Sube uno nuevo para reemplazarlo.'

    def clean_archivo(self):
        """Validar tamaño y tipo de archivo"""
        archivo = self.cleaned_data.get('archivo')
        
        # Si es edición y no se subió archivo nuevo, retornar None
        if not archivo and self.instance and self.instance.pk:
            return archivo
        
        if archivo:
            # Validar tamaño (10 MB máximo)
            max_size = 10 * 1024 * 1024  # 10 MB en bytes
            if archivo.size > max_size:
                raise ValidationError(
                    f'El archivo es demasiado grande ({archivo.size / (1024*1024):.1f} MB). '
                    f'El tamaño máximo permitido es 10 MB.'
                )
            
            # Validar extensión
            import os
            ext = os.path.splitext(archivo.name)[1].lower()
            extensiones_permitidas = [
                '.pdf', '.jpg', '.jpeg', '.png', '.gif', 
                '.doc', '.docx', '.xls', '.xlsx'
            ]
            
            if ext not in extensiones_permitidas:
                raise ValidationError(
                    f'Tipo de archivo no permitido ({ext}). '
                    f'Formatos permitidos: PDF, JPG, PNG, DOC, DOCX, XLS, XLSX.'
                )
        
        return archivo

    def clean(self):
        """Validaciones adicionales del formulario completo"""
        cleaned_data = super().clean()
        tipo_documento = cleaned_data.get('tipo_documento')
        vigencia_desde = cleaned_data.get('vigencia_desde')
        vigencia_hasta = cleaned_data.get('vigencia_hasta')
        
        # Si el tipo requiere vigencia, validar fechas
        if tipo_documento and tipo_documento.requiere_vigencia:
            if not vigencia_hasta:
                self.add_error(
                    'vigencia_hasta',
                    'Este tipo de documento requiere fecha de vencimiento.'
                )
        
        # Validar que fecha_hasta sea posterior a fecha_desde
        if vigencia_desde and vigencia_hasta:
            if vigencia_hasta < vigencia_desde:
                self.add_error(
                    'vigencia_hasta',
                    'La fecha de vencimiento debe ser posterior a la fecha de inicio.'
                )
            
            # Advertencia si la vigencia es muy corta (menos de 7 días)
            delta = vigencia_hasta - vigencia_desde
            if delta.days < 7:
                self.add_error(
                    'vigencia_hasta',
                    'La vigencia es muy corta (menos de 7 días). Verifica las fechas.'
                )
        
        # Validar que la fecha de vencimiento no esté en el pasado (solo en creación)
        if not self.instance.pk and vigencia_hasta:
            if vigencia_hasta < date.today():
                self.add_error(
                    'vigencia_hasta',
                    'La fecha de vencimiento no puede estar en el pasado.'
                )
        
        return cleaned_data

    def save(self, commit=True):
        """
        Guardar el documento.
        Automáticamente guarda el nombre original del archivo y el usuario.
        """
        instance = super().save(commit=False)
        
        # Si hay un archivo nuevo, guardar su nombre original
        if self.cleaned_data.get('archivo'):
            instance.nombre_archivo_original = self.cleaned_data['archivo'].name
        
        # Guardar el usuario que cargó el documento (si está disponible en el request)
        # Esto se puede configurar pasando el request al formulario
        # if hasattr(self, 'request') and self.request.user.is_authenticated:
        #     instance.cargado_por = self.request.user.username
        
        if commit:
            instance.save()
        
        return instance


# ================================================================
# FORMULARIO DE BÚSQUEDA/FILTRO (OPCIONAL)
# ================================================================

class DocumentoFilterForm(forms.Form):
    """
    Formulario para filtrar documentos en el listado.
    Útil para búsquedas avanzadas.
    """
    
    tipo_documento = forms.ModelChoiceField(
        queryset=TipoDocumento.objects.filter(activo=True).order_by('nombre_tipo_documento'),
        required=False,
        empty_label='-- Todos los tipos --',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Tipo de Documento'
    )
    
    estado_vigencia = forms.ChoiceField(
        choices=[
            ('', '-- Todos los estados --'),
            ('vigente', 'Vigente'),
            ('proximo_vencer', 'Próximo a vencer'),
            ('vencido', 'Vencido'),
            ('sin_control', 'Sin control de vigencia')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Estado de Vigencia'
    )
    
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='Cargado desde'
    )
    
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='Cargado hasta'
    )