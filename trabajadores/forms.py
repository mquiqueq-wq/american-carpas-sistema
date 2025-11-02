from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta

from .models import (
    TrabajadorPersonal, TrabajadorLaboral, TrabajadorAfiliaciones,
    TrabajadorDotacion, TrabajadorCurso, TrabajadorRol, TipoCurso, TipoDotacion
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