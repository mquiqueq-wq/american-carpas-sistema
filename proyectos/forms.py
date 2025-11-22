"""
Formularios para el módulo de gestión de proyectos
American Carpas 1 SAS

Formularios completos para todas las 8 fases
"""

from django import forms
from django.core.exceptions import ValidationError
from datetime import date

from trabajadores.models import TrabajadorPersonal
from .models import (
    AvanceActividad,
    TipoProyecto,
    EstadoProyecto,
    TipoDocumentoProyecto,
    Cliente,
    Proyecto,
    Actividad,
    AsignacionTrabajador,
    DocumentoProyecto,
    EvidenciaFotografica,
)


# =====================================================
# WIDGETS COMUNES
# =====================================================

TEXT_INPUT = forms.TextInput(attrs={'class': 'form-control'})
SELECT = forms.Select(attrs={'class': 'form-select'})
DATE_INPUT = forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'})
NUMBER_INPUT = forms.NumberInput(attrs={'class': 'form-control'})
EMAIL_INPUT = forms.EmailInput(attrs={'class': 'form-control'})
TEXTAREA = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
FILE_INPUT = forms.FileInput(attrs={'class': 'form-control'})
CHECKBOX = forms.CheckboxInput(attrs={'class': 'form-check-input'})


# =====================================================
# FASE 1: FORMULARIOS DE CATÁLOGOS
# =====================================================

class TipoProyectoForm(forms.ModelForm):
    """Formulario para tipos de proyectos"""
    
    nombre_tipo = forms.CharField(
        label='Nombre del Tipo de Proyecto',
        max_length=100,
        widget=TEXT_INPUT
    )
    
    descripcion = forms.CharField(
        label='Descripción',
        required=False,
        widget=TEXTAREA
    )
    
    color_identificador = forms.ChoiceField(
        label='Color Identificador',
        choices=[
            ('primary', 'Azul (Primary)'),
            ('secondary', 'Gris (Secondary)'),
            ('success', 'Verde (Success)'),
            ('danger', 'Rojo (Danger)'),
            ('warning', 'Amarillo (Warning)'),
            ('info', 'Celeste (Info)'),
        ],
        widget=SELECT
    )
    
    icono = forms.CharField(
        label='Icono Bootstrap',
        max_length=50,
        required=False,
        widget=TEXT_INPUT,
        help_text='Clase de icono Bootstrap Icons. Ej: bi-hammer'
    )
    
    activo = forms.BooleanField(
        label='Activo',
        required=False,
        initial=True,
        widget=CHECKBOX
    )
    
    class Meta:
        model = TipoProyecto
        fields = ['nombre_tipo', 'descripcion', 'color_identificador', 'icono', 'activo']


class EstadoProyectoForm(forms.ModelForm):
    """Formulario para estados de proyectos"""
    
    nombre_estado = forms.CharField(
        label='Nombre del Estado',
        max_length=50,
        widget=TEXT_INPUT
    )
    
    descripcion = forms.CharField(
        label='Descripción',
        required=False,
        widget=TEXTAREA
    )
    
    color_badge = forms.ChoiceField(
        label='Color del Badge',
        choices=[
            ('primary', 'Azul (Primary)'),
            ('secondary', 'Gris (Secondary)'),
            ('success', 'Verde (Success)'),
            ('danger', 'Rojo (Danger)'),
            ('warning', 'Amarillo (Warning)'),
            ('info', 'Celeste (Info)'),
        ],
        widget=SELECT
    )
    
    permite_edicion = forms.BooleanField(
        label='Permite Edición',
        required=False,
        initial=True,
        widget=CHECKBOX,
        help_text='Si permite editar el proyecto en este estado'
    )
    
    es_estado_final = forms.BooleanField(
        label='Es Estado Final',
        required=False,
        widget=CHECKBOX,
        help_text='Indica si es un estado final del proyecto'
    )
    
    orden_visualizacion = forms.IntegerField(
        label='Orden de Visualización',
        initial=0,
        widget=NUMBER_INPUT
    )
    
    activo = forms.BooleanField(
        label='Activo',
        required=False,
        initial=True,
        widget=CHECKBOX
    )
    
    class Meta:
        model = EstadoProyecto
        fields = ['nombre_estado', 'descripcion', 'color_badge', 'permite_edicion', 
                  'es_estado_final', 'orden_visualizacion', 'activo']


class TipoDocumentoProyectoForm(forms.ModelForm):
    """Formulario para tipos de documentos de proyectos"""
    
    nombre_tipo_documento = forms.CharField(
        label='Nombre del Tipo de Documento',
        max_length=100,
        widget=TEXT_INPUT
    )
    
    descripcion = forms.CharField(
        label='Descripción',
        required=False,
        widget=TEXTAREA
    )
    
    requiere_vigencia = forms.BooleanField(
        label='Requiere Control de Vigencia',
        required=False,
        widget=CHECKBOX,
        help_text='Si el documento tiene fecha de vencimiento'
    )
    
    dias_alerta_vencimiento = forms.IntegerField(
        label='Días de Alerta antes del Vencimiento',
        initial=30,
        widget=NUMBER_INPUT
    )
    
    icono = forms.CharField(
        label='Icono Bootstrap',
        max_length=50,
        required=False,
        widget=TEXT_INPUT
    )
    
    orden_visualizacion = forms.IntegerField(
        label='Orden de Visualización',
        initial=0,
        widget=NUMBER_INPUT
    )
    
    activo = forms.BooleanField(
        label='Activo',
        required=False,
        initial=True,
        widget=CHECKBOX
    )
    
    class Meta:
        model = TipoDocumentoProyecto
        fields = ['nombre_tipo_documento', 'descripcion', 'requiere_vigencia',
                  'dias_alerta_vencimiento', 'icono', 'orden_visualizacion', 'activo']


# =====================================================
# FASE 2: FORMULARIO DE CLIENTE
# =====================================================

class ClienteForm(forms.ModelForm):
    """Formulario para gestión de clientes"""
    
    tipo_documento = forms.ChoiceField(
        label='Tipo de Documento',
        choices=[
            ('', '-- Seleccione --'),
            ('NIT', 'NIT'),
            ('CC', 'Cédula de Ciudadanía'),
            ('CE', 'Cédula de Extranjería'),
            ('PASAPORTE', 'Pasaporte'),
        ],
        widget=SELECT
    )
    
    numero_documento = forms.CharField(
        label='Número de Documento/NIT',
        max_length=20,
        widget=TEXT_INPUT
    )
    
    razon_social = forms.CharField(
        label='Razón Social',
        max_length=200,
        widget=TEXT_INPUT
    )
    
    nombre_comercial = forms.CharField(
        label='Nombre Comercial',
        max_length=200,
        required=False,
        widget=TEXT_INPUT
    )
    
    representante_legal = forms.CharField(
        label='Representante Legal',
        max_length=150,
        required=False,
        widget=TEXT_INPUT
    )
    
    telefono_principal = forms.CharField(
        label='Teléfono Principal',
        max_length=20,
        widget=TEXT_INPUT
    )
    
    telefono_secundario = forms.CharField(
        label='Teléfono Secundario',
        max_length=20,
        required=False,
        widget=TEXT_INPUT
    )
    
    email_principal = forms.EmailField(
        label='Email Principal',
        widget=EMAIL_INPUT
    )
    
    email_secundario = forms.EmailField(
        label='Email Secundario',
        required=False,
        widget=EMAIL_INPUT
    )
    
    direccion = forms.CharField(
        label='Dirección',
        max_length=200,
        widget=TEXT_INPUT
    )
    
    ciudad = forms.CharField(
        label='Ciudad',
        max_length=100,
        widget=TEXT_INPUT
    )
    
    departamento = forms.CharField(
        label='Departamento',
        max_length=100,
        widget=TEXT_INPUT
    )
    
    pais = forms.CharField(
        label='País',
        max_length=100,
        initial='Colombia',
        widget=TEXT_INPUT
    )
    
    sitio_web = forms.URLField(
        label='Sitio Web',
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )
    
    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=TEXTAREA
    )
    
    activo = forms.BooleanField(
        label='Cliente Activo',
        required=False,
        initial=True,
        widget=CHECKBOX
    )
    
    class Meta:
        model = Cliente
        fields = ['tipo_documento', 'numero_documento', 'razon_social', 'nombre_comercial',
                  'representante_legal', 'telefono_principal', 'telefono_secundario',
                  'email_principal', 'email_secundario', 'direccion', 'ciudad',
                  'departamento', 'pais', 'sitio_web', 'observaciones', 'activo']
    
    def clean_numero_documento(self):
        """Validación del número de documento"""
        numero = self.cleaned_data.get('numero_documento')
        if numero:
            numero = numero.strip().replace(' ', '').replace('-', '')
        return numero


# =====================================================
# FASE 3: FORMULARIO DE PROYECTO
# =====================================================

class ProyectoForm(forms.ModelForm):
    """Formulario para gestión de proyectos"""
    
    cliente = forms.ModelChoiceField(
        label='Cliente',
        queryset=Cliente.objects.filter(activo=True),
        widget=SELECT,
        empty_label='-- Seleccione un cliente --'
    )
    
    tipo_proyecto = forms.ModelChoiceField(
        label='Tipo de Proyecto',
        queryset=TipoProyecto.objects.filter(activo=True),
        widget=SELECT,
        empty_label='-- Seleccione un tipo --'
    )
    
    estado_proyecto = forms.ModelChoiceField(
        label='Estado del Proyecto',
        queryset=EstadoProyecto.objects.filter(activo=True),
        widget=SELECT,
        empty_label='-- Seleccione un estado --'
    )
    
    codigo_proyecto = forms.CharField(
        label='Código del Proyecto',
        max_length=50,
        widget=TEXT_INPUT,
        help_text='Código único identificador del proyecto. Ej: PROY-2024-001'
    )
    
    nombre_proyecto = forms.CharField(
        label='Nombre del Proyecto',
        max_length=200,
        widget=TEXT_INPUT
    )
    
    descripcion = forms.CharField(
        label='Descripción del Proyecto',
        required=False,
        widget=TEXTAREA
    )
    
    ingeniero_responsable = forms.CharField(
        label='Ingeniero Responsable',
        max_length=150,
        widget=TEXT_INPUT,
        help_text='Ingeniero del cliente responsable del proyecto'
    )
    
    cargo_responsable = forms.CharField(
        label='Cargo del Responsable',
        max_length=100,
        required=False,
        widget=TEXT_INPUT
    )
    
    telefono_responsable = forms.CharField(
        label='Teléfono del Responsable',
        max_length=20,
        required=False,
        widget=TEXT_INPUT
    )
    
    email_responsable = forms.EmailField(
        label='Email del Responsable',
        required=False,
        widget=EMAIL_INPUT
    )
    
    direccion_proyecto = forms.CharField(
        label='Dirección del Proyecto',
        max_length=200,
        widget=TEXT_INPUT
    )
    
    ciudad_proyecto = forms.CharField(
        label='Ciudad del Proyecto',
        max_length=100,
        widget=TEXT_INPUT
    )
    
    departamento_proyecto = forms.CharField(
        label='Departamento del Proyecto',
        max_length=100,
        widget=TEXT_INPUT
    )
    
    fecha_inicio = forms.DateField(
        label='Fecha de Inicio',
        widget=DATE_INPUT
    )
    
    fecha_fin_estimada = forms.DateField(
        label='Fecha de Fin Estimada',
        widget=DATE_INPUT
    )
    
    fecha_fin_real = forms.DateField(
        label='Fecha de Fin Real',
        required=False,
        widget=DATE_INPUT
    )
    
    presupuesto_estimado = forms.DecimalField(
        label='Presupuesto Estimado',
        max_digits=15,
        decimal_places=2,
        required=False,
        widget=NUMBER_INPUT,
        help_text='Presupuesto estimado del proyecto en COP'
    )
    
    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=TEXTAREA
    )
    
    activo = forms.BooleanField(
        label='Proyecto Activo',
        required=False,
        initial=True,
        widget=CHECKBOX
    )
    
    class Meta:
        model = Proyecto
        fields = [
            'cliente', 'tipo_proyecto', 'estado_proyecto', 'codigo_proyecto',
            'nombre_proyecto', 'descripcion', 'ingeniero_responsable', 'cargo_responsable',
            'telefono_responsable', 'email_responsable', 'direccion_proyecto',
            'ciudad_proyecto', 'departamento_proyecto', 'fecha_inicio',
            'fecha_fin_estimada', 'fecha_fin_real', 'presupuesto_estimado',
            'observaciones', 'activo'
        ]
    
    def clean(self):
        """Validaciones cruzadas"""
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin_estimada = cleaned_data.get('fecha_fin_estimada')
        fecha_fin_real = cleaned_data.get('fecha_fin_real')
        
        # Validar que fecha fin estimada sea posterior a fecha inicio
        if fecha_inicio and fecha_fin_estimada:
            if fecha_fin_estimada <= fecha_inicio:
                raise ValidationError(
                    'La fecha de finalización estimada debe ser posterior a la fecha de inicio.'
                )
        
        # Validar fecha fin real si existe
        if fecha_fin_real and fecha_inicio:
            if fecha_fin_real < fecha_inicio:
                raise ValidationError(
                    'La fecha de finalización real no puede ser anterior a la fecha de inicio.'
                )
        
        return cleaned_data


# =====================================================
# FASE 4: FORMULARIO DE ACTIVIDAD
# =====================================================

class ActividadForm(forms.ModelForm):
    """Formulario para gestión de actividades con soporte de jerarquía padre-hijo"""
    
    proyecto = forms.ModelChoiceField(
        label='Proyecto',
        queryset=Proyecto.objects.filter(activo=True),
        widget=SELECT,
        empty_label='-- Seleccione un proyecto --'
    )
    
    actividad_padre = forms.ModelChoiceField(
        label='Actividad Padre (Opcional)',
        queryset=Actividad.objects.filter(activo=True),
        required=False,
        widget=SELECT,
        empty_label='-- Sin actividad padre (es actividad principal) --',
        help_text='Si esta es una etapa/subdivisión, seleccione la actividad general'
    )
    
    numero_actividad = forms.CharField(
        label='Número de Actividad',
        max_length=20,
        widget=TEXT_INPUT,
        help_text='Ej: 4 (padre), 4.1 (hijo), 4.2 (hijo)'
    )
    
    nombre_actividad = forms.CharField(
        label='Nombre de la Actividad',
        max_length=200,
        widget=TEXT_INPUT,
        help_text='Ej: "Instalación de bordillo" (padre) o "Bordillo etapa 1" (hijo)'
    )
    
    descripcion = forms.CharField(
        label='Descripción',
        required=False,
        widget=TEXTAREA
    )
    
    unidad_medida = forms.ChoiceField(
        label='Unidad de Medida',
        choices=[
            ('M', 'Metro (m)'),
            ('M2', 'Metro cuadrado (m²)'),
            ('M3', 'Metro cúbico (m³)'),
            ('UND', 'Unidad'),
            ('GLB', 'Global'),
            ('pto', 'Punto'),
            ('KG', 'Kilogramo'),
            ('L', 'Litro'),
            ('H', 'Hora'),
            ('OTRO', 'Otro'),
        ],
        widget=SELECT
    )

    cantidad_programada = forms.DecimalField(
        label='Cantidad Programada',
        max_digits=12,
        decimal_places=2,
        initial=0,
        widget=NUMBER_INPUT,
        help_text='Solo para actividades hijas. Las actividades padre suman automáticamente'
    )
    
    porcentaje_avance = forms.DecimalField(
        label='Porcentaje de Avance',
        max_digits=5,
        decimal_places=2,
        required=False,
        widget=NUMBER_INPUT,
        help_text='Se actualiza automáticamente según los avances registrados',
        disabled=True
    )
    
    peso_actividad = forms.DecimalField(
        label='Peso de la Actividad',
        max_digits=5,
        decimal_places=2,
        initial=1,
        widget=NUMBER_INPUT,
        help_text='Peso relativo para cálculo de avance del proyecto'
    )
    
    fecha_inicio_estimada = forms.DateField(
        label='Fecha Inicio Estimada',
        required=False,
        widget=DATE_INPUT
    )
    
    fecha_fin_estimada = forms.DateField(
        label='Fecha Fin Estimada',
        required=False,
        widget=DATE_INPUT
    )
    
    fecha_inicio_real = forms.DateField(
        label='Fecha Inicio Real',
        required=False,
        widget=DATE_INPUT
    )
    
    fecha_fin_real = forms.DateField(
        label='Fecha Fin Real',
        required=False,
        widget=DATE_INPUT
    )
    
    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=TEXTAREA
    )
    
    orden_visualizacion = forms.IntegerField(
        label='Orden de Visualización',
        initial=0,
        widget=NUMBER_INPUT
    )
    
    activo = forms.BooleanField(
        label='Actividad Activa',
        required=False,
        initial=True,
        widget=CHECKBOX
    )
    
    class Meta:
        model = Actividad
        fields = [
            'proyecto', 'actividad_padre', 'numero_actividad', 'nombre_actividad',
            'descripcion', 'unidad_medida', 'cantidad_programada', 'porcentaje_avance', 'peso_actividad',
            'fecha_inicio_estimada', 'fecha_fin_estimada', 'fecha_inicio_real',
            'fecha_fin_real', 'observaciones', 'orden_visualizacion', 'activo'
        ]
    
    def __init__(self, *args, **kwargs):
        # ✅ CORRECCIÓN: Extraer el proyecto si viene como parámetro
        proyecto = kwargs.pop('proyecto', None)
        super().__init__(*args, **kwargs)
        
        # Configurar el queryset de actividad_padre
        if proyecto:
            # Si se pasa el proyecto como parámetro (creación)
            self.fields['proyecto'].initial = proyecto
            self.fields['proyecto'].widget = forms.HiddenInput()
            # Filtrar actividades padre del mismo proyecto
            self.fields['actividad_padre'].queryset = Actividad.objects.filter(
                proyecto=proyecto,
                activo=True,
                actividad_padre__isnull=True  # Solo actividades principales pueden ser padre
            )
        elif self.instance and self.instance.pk:
            # Si estamos editando
            if self.instance.proyecto:
                # Solo mostrar actividades del mismo proyecto que NO tengan padre
                self.fields['actividad_padre'].queryset = Actividad.objects.filter(
                    proyecto=self.instance.proyecto,
                    activo=True,
                    actividad_padre__isnull=True
                ).exclude(pk=self.instance.pk)  # No puede ser padre de sí misma
        else:
            # Si no hay proyecto, dejar vacío
            self.fields['actividad_padre'].queryset = Actividad.objects.none()
    
    def clean(self):
        """Validaciones personalizadas"""
        cleaned_data = super().clean()
        
        # Validar fechas estimadas
        fecha_inicio = cleaned_data.get('fecha_inicio_estimada')
        fecha_fin = cleaned_data.get('fecha_fin_estimada')
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise ValidationError(
                    'La fecha de fin estimada no puede ser anterior a la fecha de inicio.'
                )
        
        # Validar fechas reales
        fecha_inicio_real = cleaned_data.get('fecha_inicio_real')
        fecha_fin_real = cleaned_data.get('fecha_fin_real')
        if fecha_inicio_real and fecha_fin_real:
            if fecha_fin_real < fecha_inicio_real:
                raise ValidationError(
                    'La fecha de fin real no puede ser anterior a la fecha de inicio real.'
                )
        
        return cleaned_data

# ====
# FASE 4.1: FORMULARIO DE AVANCE DE ACTIVIDAD
# ====

class AvanceActividadForm(forms.ModelForm):
    """Formulario para registrar avances de una actividad"""

    actividad = forms.ModelChoiceField(
        label='Actividad',
        queryset=Actividad.objects.filter(activo=True),
        widget=SELECT,
        empty_label='-- Seleccione una actividad --'
    )

    fecha_avance = forms.DateField(
        label='Fecha del Avance',
        widget=DATE_INPUT
    )

    cantidad_ejecutada = forms.DecimalField(
        label='Cantidad Ejecutada en el Período',
        max_digits=12,
        decimal_places=2,
        widget=NUMBER_INPUT
    )

    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=TEXTAREA
    )

    class Meta:
        model = AvanceActividad
        fields = ['actividad', 'fecha_avance', 'cantidad_ejecutada', 'observaciones']

    def __init__(self, *args, **kwargs):
        actividad = kwargs.pop('actividad', None)
        super().__init__(*args, **kwargs)

        # Si se pasa la actividad desde la vista, ocultamos el campo y lo fijamos
        if actividad is not None:
            self.fields['actividad'].initial = actividad
            self.fields['actividad'].widget = forms.HiddenInput()

    def clean_cantidad_ejecutada(self):
        cantidad = self.cleaned_data.get('cantidad_ejecutada')
        if cantidad is not None and cantidad < 0:
            raise ValidationError('La cantidad ejecutada no puede ser negativa.')
        return cantidad

# =====================================================
# FASE 5: FORMULARIO DE ASIGNACIÓN DE TRABAJADOR
# =====================================================

class AsignacionTrabajadorForm(forms.ModelForm):
    """Formulario para asignar trabajadores a proyectos"""

    proyecto = forms.ModelChoiceField(
        label='Proyecto',
        queryset=Proyecto.objects.filter(activo=True),
        widget=SELECT,
        empty_label='-- Seleccione un proyecto --'
    )

    trabajador = forms.ModelChoiceField(
        label='Trabajador',
        queryset=TrabajadorPersonal.objects.all(),  # filtramos en la vista
        widget=SELECT,
        empty_label='-- Seleccione un trabajador --'
    )

    fecha_asignacion = forms.DateField(
        label='Fecha de Asignación',
        widget=DATE_INPUT
    )

    fecha_desasignacion = forms.DateField(
        label='Fecha de Desasignación',
        required=False,
        widget=DATE_INPUT,
        help_text='Dejar vacío si aún está asignado'
    )

    rol_en_proyecto = forms.CharField(
        label='Rol en el Proyecto',
        max_length=100,
        required=False,
        widget=TEXT_INPUT,
        help_text='Ej: Operario, Ayudante, Supervisor'
    )

    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=TEXTAREA
    )

    activo = forms.BooleanField(
        label='Asignación Activa',
        required=False,
        initial=True,
        widget=CHECKBOX
    )

    class Meta:
        model = AsignacionTrabajador
        fields = [
            'proyecto',          # lo ocultamos
            'trabajador',
            'fecha_asignacion',
            'fecha_desasignacion',
            'rol_en_proyecto',
            'observaciones',
            'activo',
        ]

    def __init__(self, *args, **kwargs):
        proyecto = kwargs.pop('proyecto', None)
        trabajadores_qs = kwargs.pop('trabajadores_qs', None)
        super().__init__(*args, **kwargs)

        if proyecto is not None:
            self.fields['proyecto'].initial = proyecto
            self.fields['proyecto'].widget = forms.HiddenInput()

        if trabajadores_qs is not None:
            self.fields['trabajador'].queryset = trabajadores_qs

    def clean(self):
        """Validar que fecha desasignación sea posterior a asignación
        y que no existan asignaciones solapadas para el mismo trabajador y proyecto.
        """
        cleaned_data = super().clean()
        fecha_asignacion = cleaned_data.get('fecha_asignacion')
        fecha_desasignacion = cleaned_data.get('fecha_desasignacion')
        trabajador = cleaned_data.get('trabajador')
        proyecto = cleaned_data.get('proyecto')

        # 1) Validar orden de fechas
        if fecha_asignacion and fecha_desasignacion:
            if fecha_desasignacion < fecha_asignacion:
                raise ValidationError(
                    'La fecha de desasignación no puede ser anterior a la fecha de asignación.'
                )

        # 2) Evitar solapamiento de asignaciones del mismo trabajador al mismo proyecto
        if trabajador and proyecto and fecha_asignacion:
            # Rango de esta asignación
            inicio_nuevo = fecha_asignacion
            fin_nuevo = fecha_desasignacion  # puede ser None

            # Buscar otras asignaciones del mismo trabajador y proyecto
            qs = AsignacionTrabajador.objects.filter(
                trabajador=trabajador,
                proyecto=proyecto
            )

            # Excluirse a sí mismo si estamos editando
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            # Lógica de solapamiento:
            # Se solapan si:
            #   (fin_nuevo is None  y (otro.fin is None o otro.fin >= inicio_nuevo))
            #   o (ambos tienen fin y los intervalos se cruzan)
            conflictos = []
            for a in qs:
                inicio_otro = a.fecha_asignacion
                fin_otro = a.fecha_desasignacion

                # Caso 1: esta asignación no tiene fin (sigue abierta)
                if fin_nuevo is None:
                    # Se solapa si el otro no tiene fin o termina después o igual que mi inicio
                    if fin_otro is None or fin_otro >= inicio_nuevo:
                        conflictos.append(a)
                else:
                    # Caso 2: esta asignación tiene fin
                    # Se solapa si los rangos [inicio_nuevo, fin_nuevo] y 
                    # [inicio_otro, fin_otro o infinito] se cruzan
                    if fin_otro is None:
                        # El otro sigue abierto -> se solapa si su inicio <= fin_nuevo
                        if inicio_otro <= fin_nuevo:
                            conflictos.append(a)
                    else:
                        # Ambos tienen fin
                        if inicio_otro <= fin_nuevo and fin_otro >= inicio_nuevo:
                            conflictos.append(a)

            if conflictos:
                raise ValidationError(
                    'Ya existe otra asignación activa del mismo trabajador '
                    'en este proyecto para el período indicado.'
                )

        return cleaned_data

# =====================================================
# FASE 6: FORMULARIO DE DOCUMENTO DE PROYECTO
# =====================================================

class DocumentoProyectoForm(forms.ModelForm):
    """Formulario para documentos de proyectos"""
    
    proyecto = forms.ModelChoiceField(
        label='Proyecto',
        queryset=Proyecto.objects.filter(activo=True),
        widget=SELECT,
        empty_label='-- Seleccione un proyecto --'
    )
    
    tipo_documento = forms.ModelChoiceField(
        label='Tipo de Documento',
        queryset=TipoDocumentoProyecto.objects.filter(activo=True),
        widget=SELECT,
        empty_label='-- Seleccione un tipo --'
    )
    
    nombre_documento = forms.CharField(
        label='Nombre del Documento',
        max_length=200,
        widget=TEXT_INPUT
    )
    
    numero_documento = forms.CharField(
        label='Número de Documento',
        max_length=100,
        required=False,
        widget=TEXT_INPUT,
        help_text='Número de radicado, consecutivo, etc.'
    )
    
    descripcion = forms.CharField(
        label='Descripción',
        required=False,
        widget=TEXTAREA
    )
    
    archivo = forms.FileField(
        label='Archivo',
        widget=FILE_INPUT
    )
    
    fecha_emision = forms.DateField(
        label='Fecha de Emisión',
        required=False,
        widget=DATE_INPUT
    )
    
    fecha_vencimiento = forms.DateField(
        label='Fecha de Vencimiento',
        required=False,
        widget=DATE_INPUT
    )
    
    activo = forms.BooleanField(
        label='Documento Activo',
        required=False,
        initial=True,
        widget=CHECKBOX
    )
    
    class Meta:
        model = DocumentoProyecto
        fields = ['proyecto', 'tipo_documento', 'nombre_documento', 'numero_documento',
                  'descripcion', 'archivo', 'fecha_emision', 'fecha_vencimiento', 'activo']
    
    def clean(self):
        """Validar fechas del documento"""
        cleaned_data = super().clean()
        fecha_emision = cleaned_data.get('fecha_emision')
        fecha_vencimiento = cleaned_data.get('fecha_vencimiento')
        
        if fecha_emision and fecha_vencimiento:
            if fecha_vencimiento < fecha_emision:
                raise ValidationError(
                    'La fecha de vencimiento no puede ser anterior a la fecha de emisión.'
                )
        
        return cleaned_data


# =====================================================
# FASE 7: FORMULARIO DE EVIDENCIA FOTOGRÁFICA
# =====================================================

class EvidenciaFotograficaForm(forms.ModelForm):
    """Formulario para evidencias fotográficas"""
    
    proyecto = forms.ModelChoiceField(
        label='Proyecto',
        queryset=Proyecto.objects.filter(activo=True),
        widget=SELECT,
        empty_label='-- Seleccione un proyecto --'
    )
    
    actividad = forms.ModelChoiceField(
        label='Actividad Relacionada',
        queryset=Actividad.objects.filter(activo=True),
        required=False,
        widget=SELECT,
        empty_label='-- Sin actividad relacionada --'
    )
    
    titulo = forms.CharField(
        label='Título',
        max_length=200,
        widget=TEXT_INPUT
    )
    
    descripcion = forms.CharField(
        label='Descripción',
        required=False,
        widget=TEXTAREA
    )
    
    tipo_evidencia = forms.ChoiceField(
        label='Tipo de Evidencia',
        choices=[
            ('', '-- Seleccione --'),
            ('INICIO', 'Inicio del Proyecto'),
            ('AVANCE', 'Avance de Obra'),
            ('PROBLEMA', 'Problema o Incidencia'),
            ('SOLUCION', 'Solución Aplicada'),
            ('CALIDAD', 'Control de Calidad'),
            ('FINAL', 'Finalización del Proyecto'),
            ('OTRO', 'Otro'),
        ],
        widget=SELECT
    )
    
    imagen = forms.ImageField(
        label='Imagen',
        widget=FILE_INPUT
    )
    
    fecha_captura = forms.DateField(
        label='Fecha de Captura',
        widget=DATE_INPUT
    )
    
    ubicacion_descripcion = forms.CharField(
        label='Ubicación',
        max_length=200,
        required=False,
        widget=TEXT_INPUT,
        help_text='Descripción de la ubicación donde se tomó la foto'
    )
    
    activo = forms.BooleanField(
        label='Evidencia Activa',
        required=False,
        initial=True,
        widget=CHECKBOX
    )
    
    class Meta:
        model = EvidenciaFotografica
        fields = ['proyecto', 'actividad', 'titulo', 'descripcion', 'tipo_evidencia',
                  'imagen', 'fecha_captura', 'ubicacion_descripcion', 'activo']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando, filtrar actividades del mismo proyecto
        if self.instance and self.instance.pk and self.instance.proyecto:
            self.fields['actividad'].queryset = Actividad.objects.filter(
                proyecto=self.instance.proyecto,
                activo=True
            )
