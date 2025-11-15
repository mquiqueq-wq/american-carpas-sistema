from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from datetime import date, timedelta

doc_validator = RegexValidator(regex=r'^\d{5,20}$', message='Solo dígitos, entre 5 y 20 caracteres.')

# CHOICES
TIPO_DOCUMENTO_CHOICES = [
    ('CC', 'Cédula de Ciudadanía'),
    ('CE', 'Cédula de Extranjería'),
    ('PPT', 'Permiso por Proteccion Temporal'),
    ('PA', 'Pasaporte'),
]

GENERO_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ('O', 'Otro / No especifica'),
]

ESTADO_CIVIL_CHOICES = [
    ('SOLTERO', 'Soltero(a)'),
    ('CASADO', 'Casado(a)'),
    ('UNION_LIBRE', 'Unión libre'),
    ('DIVORCIADO', 'Divorciado(a)'),
    ('VIUDO', 'Viudo(a)'),
]

TIPO_CUENTA_CHOICES = [
    ('AHORROS', 'Ahorros'),
    ('CORRIENTE', 'Corriente'),
    ('OTRA', 'Otra'),
]

TIPO_CONTRATO_CHOICES = [
    ('INDEFINIDO', 'Indefinido'),
    ('FIJO', 'Término Fijo'),
    ('OBRA', 'Obra o Labor'),
    ('PRESTACION', 'Prestación de Servicios'),
]

JORNADA_CHOICES = [
    ('TIEMPO_COMPLETO', 'Tiempo completo'),
    ('MEDIO_TIEMPO', 'Medio tiempo'),
    ('TURNOS', 'Por turnos'),
    ('OTRA', 'Otra'),
]

ESTADO_CUENTA_CHOICES = [
    ('ACTIVA', 'Activa'),
    ('SUSPENDIDA', 'Suspendida'),
    ('BLOQUEADA', 'Bloqueada'),
]

# Dotaciones
ESTADO_DOTACION_CHOICES = [
    ('ACTIVO', 'Activo (En uso)'),
    ('DEVUELTO', 'Devuelto'),
    ('DETERIORADO', 'Deteriorado'),
    ('EXTRAVIADO', 'Extraviado'),
]

MOTIVO_RENOVACION_DOTACION_CHOICES = [
    ('VENCIMIENTO', 'Vencimiento por tiempo'),
    ('DETERIORO', 'Deterioro'),
    ('PERDIDA', 'Pérdida o extravío'),
    ('CAMBIO_TALLA', 'Cambio de talla'),
]


class TrabajadorPersonal(models.Model):
    id_trabajador = models.CharField(
        primary_key=True,
        max_length=20,
        validators=[doc_validator],
        verbose_name="Número de Documento"
    )
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    fecha_expedicion_doc = models.DateField()
    lugar_expedicion = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    lugar_nacimiento = models.CharField(max_length=50)
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES, blank=True, null=True)
    estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES)
    direccion_residencia = models.CharField(max_length=100)
    ciudad_residencia = models.CharField(max_length=100)
    departamento_residencia = models.CharField(max_length=50)
    telefono_celular = models.CharField(max_length=20)
    correo_personal = models.CharField(max_length=50)
    grupo_sanguineo_rh = models.CharField(max_length=10)
    nombres_padre = models.CharField(max_length=100, blank=True, null=True)
    nombres_madre = models.CharField(max_length=100, blank=True, null=True)
    nombre_contacto_emergencia = models.CharField(max_length=100)
    numero_contacto_emergencia = models.CharField(max_length=40)
    numero_hijos = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    cuenta_bancaria = models.CharField(max_length=50)
    tipo_cuenta = models.CharField(max_length=20, choices=TIPO_CUENTA_CHOICES)
    banco = models.CharField(max_length=50)

    class Meta:
        db_table = 'trabajadores_personal'
        verbose_name = 'Trabajador (Datos Personales)'
        verbose_name_plural = 'Trabajadores (Datos Personales)'

    def __str__(self):
        return f"{self.nombres} {self.apellidos} (Doc: {self.id_trabajador})"

    def cursos_proximos_vencer(self, dias=30):
        return [c for c in self.cursos.all() if c.dias_para_vencer() is not None and 0 <= c.dias_para_vencer() <= dias]

    def cursos_vencidos(self):
        return [c for c in self.cursos.all() if c.dias_para_vencer() is not None and c.dias_para_vencer() < 0]

    def dotaciones_proximas_vencer(self, dias=30):
        return [d for d in self.dotaciones.filter(estado='ACTIVO') if d.dias_para_vencer() is not None and 0 <= d.dias_para_vencer() <= dias]

    def tiene_documentacion_completa(self):
        cursos_vigentes = all(c.get_estado_vigencia() == 'vigente' for c in self.cursos.all() if c.tipo_curso)
        tiene_dotacion = self.dotaciones.filter(estado='ACTIVO').exists()
        return cursos_vigentes and tiene_dotacion


class TrabajadorLaboral(models.Model):
    id_laboral = models.AutoField(primary_key=True)
    id_trabajador = models.ForeignKey(
        TrabajadorPersonal,
        on_delete=models.CASCADE,
        db_column='id_trabajador',
        related_name='registros_laborales'
    )
    tipo_contrato = models.CharField(max_length=50, choices=TIPO_CONTRATO_CHOICES)
    fecha_inicio_contrato = models.DateField()
    cargo = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=15, decimal_places=2)
    jornada_laboral = models.CharField(max_length=50, choices=JORNADA_CHOICES)
    sede_trabajo = models.CharField(max_length=100)
    fecha_terminacion_contrato = models.DateField(blank=True, null=True)
    motivo_terminacion = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'trabajadores_laboral'
        verbose_name = 'Registro Laboral'
        verbose_name_plural = 'Registros Laborales'

    def __str__(self):
        return f"{self.id_trabajador.nombres} {self.id_trabajador.apellidos} - {self.cargo}"


class TrabajadorAfiliaciones(models.Model):
    id_afiliacion = models.AutoField(primary_key=True)
    id_trabajador = models.ForeignKey(
        TrabajadorPersonal,
        on_delete=models.CASCADE,
        db_column='id_trabajador',
        related_name='afiliaciones'
    )
    eps_nombre = models.CharField(max_length=100)
    eps_numero_afiliacion = models.CharField(max_length=50)
    fondo_pensiones_nombre = models.CharField(max_length=100)
    fondo_pensiones_numero_afiliacion = models.CharField(max_length=50)
    arl_nombre = models.CharField(max_length=100)
    arl_numero_nombre = models.CharField(max_length=50)
    caja_compensacion_nombre = models.CharField(max_length=100)
    caja_compensacion_numero_afiliacion = models.CharField(max_length=50)

    class Meta:
        db_table = 'trabajadores_afiliaciones'
        verbose_name = 'Afiliación'
        verbose_name_plural = 'Afiliaciones'

    def __str__(self):
        return f"Afiliaciones de {self.id_trabajador}"


class TipoDotacion(models.Model):
    id_tipo_dotacion = models.AutoField(primary_key=True)
    nombre_tipo_dotacion = models.CharField(
        max_length=100,
        unique=True,
        help_text="Ej: Casco, Botas de seguridad, Arnés"
    )
    vida_util_dias = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Días de vida útil estándar del elemento"
    )
    descripcion = models.TextField(blank=True, null=True)
    requiere_talla = models.BooleanField(default=True)
    tallas_disponibles = models.TextField(
        blank=True,
        null=True,
        help_text='Tallas separadas por comas. Ej: 32,34,36,38 o S,M,L,XL'
    )
    normativa_referencia = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Ej: Resolución 2400 de 1979"
    )
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'tipos_dotaciones'
        verbose_name = 'Tipo de Dotación'
        verbose_name_plural = 'Tipos de Dotaciones'
        ordering = ['nombre_tipo_dotacion']

    def __str__(self):
        return self.nombre_tipo_dotacion

    def get_tallas_lista(self):
        if not self.tallas_disponibles:
            return []
        tallas = [t.strip() for t in self.tallas_disponibles.split(',')]
        return [t for t in tallas if t]

    def get_tallas_choices(self):
        if not self.requiere_talla:
            return [('N/A', 'No aplica')]
        tallas = self.get_tallas_lista()
        if not tallas:
            return [('', '-- Sin tallas configuradas --')]
        choices = [('', '-- Seleccione una talla --')]
        choices.extend([(t, t) for t in tallas])
        return choices

    def get_tallas_json(self):
        import json
        if not self.requiere_talla:
            return json.dumps([['N/A', 'No aplica']])
        tallas = self.get_tallas_lista()
        if not tallas:
            return json.dumps([['', 'Sin tallas configuradas']])
        tallas_json = [['', '-- Seleccione una talla --']]
        tallas_json.extend([[t, t] for t in tallas])
        return json.dumps(tallas_json)

    def es_talla_valida(self, talla):
        if not self.requiere_talla:
            return talla == 'N/A'
        tallas_validas = self.get_tallas_lista()
        return talla in tallas_validas


class TrabajadorDotacion(models.Model):
    id_dotacion = models.AutoField(primary_key=True)
    id_trabajador = models.ForeignKey(
        TrabajadorPersonal,
        on_delete=models.CASCADE,
        db_column='id_trabajador',
        related_name='dotaciones'
    )
    tipo_dotacion_catalogo = models.ForeignKey(
        TipoDotacion,
        on_delete=models.PROTECT,
        related_name='dotaciones_entregadas',
        null=True,
        blank=True,
        help_text="Tipo de dotación del catálogo"
    )
    # Campo legacy para compatibilidad
    tipo_dotacion = models.CharField(max_length=100)
    talla = models.CharField(
        max_length=20,
        blank=True,
        help_text="Talla del elemento (validada según el tipo de dotación)"
    )
    fecha_entrega = models.DateField()
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_DOTACION_CHOICES,
        default='ACTIVO'
    )
    fecha_vencimiento = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha calculada de vencimiento"
    )
    fecha_devolucion = models.DateField(null=True, blank=True)
    motivo_devolucion = models.CharField(
        max_length=20,
        choices=MOTIVO_RENOVACION_DOTACION_CHOICES,
        null=True,
        blank=True
    )
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'trabajadores_dotacion'
        verbose_name = 'Dotación'
        verbose_name_plural = 'Dotaciones'

    def __str__(self):
        return f"{self.tipo_dotacion} - {self.id_trabajador} ({self.fecha_entrega})"

    def save(self, *args, **kwargs):
        if self.tipo_dotacion_catalogo and not self.fecha_vencimiento:
            self.fecha_vencimiento = self.fecha_entrega + timedelta(days=self.tipo_dotacion_catalogo.vida_util_dias)
        super().save(*args, **kwargs)

    def calcular_fecha_vencimiento(self):
        if self.fecha_vencimiento:
            return self.fecha_vencimiento
        if self.tipo_dotacion_catalogo:
            return self.fecha_entrega + timedelta(days=self.tipo_dotacion_catalogo.vida_util_dias)
        return None

    def dias_para_vencer(self):
        fecha_venc = self.calcular_fecha_vencimiento()
        if fecha_venc and self.estado == 'ACTIVO':
            delta = fecha_venc - date.today()
            return delta.days
        return None

    def get_estado_vigencia(self):
        if self.estado != 'ACTIVO':
            return 'inactivo'
        dias = self.dias_para_vencer()
        if dias is None:
            return 'sin_configurar'
        elif dias < 0:
            return 'vencido'
        elif dias <= 30:
            return 'proximo_vencer'
        else:
            return 'vigente'

    def get_estado_display_vigencia(self):
        estados = {
            'vigente': 'Vigente',
            'proximo_vencer': 'Próximo a vencer',
            'vencido': 'Vencido',
            'inactivo': 'Inactivo',
            'sin_configurar': 'Sin configurar'
        }
        return estados.get(self.get_estado_vigencia(), 'Desconocido')

    def get_color_estado(self):
        colores = {
            'vigente': 'success',
            'proximo_vencer': 'warning',
            'vencido': 'danger',
            'inactivo': 'secondary',
            'sin_configurar': 'secondary'
        }
        return colores.get(self.get_estado_vigencia(), 'secondary')


class TipoCurso(models.Model):
    id_tipo_curso = models.AutoField(primary_key=True)
    nombre_tipo_curso = models.CharField(max_length=200, unique=True)
    vigencia_dias = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Días de vigencia del curso"
    )
    requiere_renovacion = models.BooleanField(default=True)
    normativa_referencia = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Ej: Resolución 1409 de 2012 - Trabajo en Alturas"
    )
    dias_alerta_anticipada = models.IntegerField(
        default=30,
        validators=[MinValueValidator(1)],
        help_text="Días antes del vencimiento para enviar alerta"
    )
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'tipos_cursos'
        verbose_name = 'Tipo de Curso'
        verbose_name_plural = 'Tipos de Cursos'
        ordering = ['nombre_tipo_curso']

    def __str__(self):
        return f"{self.nombre_tipo_curso} ({self.vigencia_dias} días)"


class TrabajadorCurso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    id_trabajador = models.ForeignKey(
        TrabajadorPersonal,
        on_delete=models.CASCADE,
        db_column='id_trabajador',
        related_name='cursos'
    )
    tipo_curso = models.ForeignKey(
        TipoCurso,
        on_delete=models.PROTECT,
        related_name='cursos_realizados',
        null=True,
        blank=True,
        help_text="Tipo de curso (requerido para control de vigencia)"
    )
    nombre_curso = models.CharField(max_length=200)
    institucion = models.CharField(max_length=150)
    fecha_inicio_curso = models.DateField()
    fecha_fin_curso = models.DateField(blank=True, null=True)
    certificado_url = models.CharField(max_length=260, blank=True, null=True)
    numero_certificado = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Número del certificado oficial"
    )
    es_renovacion_de = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='renovaciones',
        help_text="Curso anterior que este renueva"
    )

    class Meta:
        db_table = 'trabajadores_cursos'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return f"{self.nombre_curso} - {self.id_trabajador}"

    def calcular_fecha_vencimiento(self):
        if self.tipo_curso and self.fecha_fin_curso:
            return self.fecha_fin_curso + timedelta(days=self.tipo_curso.vigencia_dias)
        return None

    def dias_para_vencer(self):
        fecha_venc = self.calcular_fecha_vencimiento()
        if fecha_venc:
            delta = fecha_venc - date.today()
            return delta.days
        return None

    def get_estado_vigencia(self):
        if not self.tipo_curso:
            return 'sin_configurar'
        dias = self.dias_para_vencer()
        if dias is None:
            return 'sin_configurar'
        elif dias < 0:
            return 'vencido'
        elif dias <= (self.tipo_curso.dias_alerta_anticipada or 30):
            return 'proximo_vencer'
        else:
            return 'vigente'

    def get_estado_display(self):
        estados = {
            'vigente': 'Vigente',
            'proximo_vencer': 'Próximo a vencer',
            'vencido': 'Vencido',
            'sin_configurar': 'Sin configurar'
        }
        return estados.get(self.get_estado_vigencia(), 'Desconocido')

    def get_color_estado(self):
        colores = {
            'vigente': 'success',
            'proximo_vencer': 'warning',
            'vencido': 'danger',
            'sin_configurar': 'secondary'
        }
        return colores.get(self.get_estado_vigencia(), 'secondary')


class TrabajadorRol(models.Model):
    id_rol_sistema = models.AutoField(primary_key=True)
    id_trabajador = models.ForeignKey(
        TrabajadorPersonal,
        on_delete=models.CASCADE,
        db_column='id_trabajador',
        related_name='roles_sistema'
    )
    rol_sistema = models.CharField(max_length=50)
    estado_cuenta = models.CharField(max_length=20, choices=ESTADO_CUENTA_CHOICES)
    ultimo_inicio_sesion = models.DateTimeField(blank=True, null=True)
    password_hash = models.CharField(max_length=255)

    class Meta:
        db_table = 'trabajadores_rol'
        verbose_name = 'Rol de Sistema'
        verbose_name_plural = 'Roles de Sistema'

    def __str__(self):
        return f"{self.id_trabajador} - {self.rol_sistema}"
class TipoDocumento(models.Model):
    """
    Catálogo de tipos de documentos que pueden ser adjuntados a los trabajadores.
    Ejemplos: Fotocopia CC, Certificado Curso, Afiliación EPS, etc.
    """
    id_tipo_documento = models.AutoField(primary_key=True)
    nombre_tipo_documento = models.CharField(
        max_length=100,
        verbose_name="Nombre del Tipo de Documento",
        help_text="Ej: Fotocopia Cédula, Certificado Curso, Afiliación EPS"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción",
        help_text="Descripción detallada del tipo de documento"
    )
    es_obligatorio = models.BooleanField(
        default=False,
        verbose_name="¿Es obligatorio?",
        help_text="Indica si este documento es obligatorio para todos los trabajadores"
    )
    requiere_vigencia = models.BooleanField(
        default=False,
        verbose_name="¿Requiere control de vigencia?",
        help_text="Indica si el documento tiene fecha de vencimiento"
    )
    icono_bootstrap = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Icono Bootstrap",
        help_text="Ej: bi-file-earmark-text, bi-card-checklist"
    )
    orden_visualizacion = models.IntegerField(
        default=0,
        verbose_name="Orden de visualización",
        help_text="Orden en que se muestra en el detalle del trabajador (menor = primero)"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Si está activo, aparecerá disponible para asignar"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tipos_documentos'
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documentos'
        ordering = ['orden_visualizacion', 'nombre_tipo_documento']

    def __str__(self):
        return self.nombre_tipo_documento

    def count_documentos_activos(self):
        """Retorna la cantidad de documentos activos de este tipo"""
        return self.documentos_trabajadores.count()


class TrabajadorDocumento(models.Model):
    """
    Documentos adjuntos a cada trabajador (PDFs, imágenes, etc.)
    """
    id_documento = models.AutoField(primary_key=True)
    id_trabajador = models.ForeignKey(
        TrabajadorPersonal,
        on_delete=models.CASCADE,
        db_column='id_trabajador',
        related_name='documentos',
        verbose_name="Trabajador"
    )
    tipo_documento = models.ForeignKey(
        TipoDocumento,
        on_delete=models.PROTECT,
        related_name='documentos_trabajadores',
        verbose_name="Tipo de Documento",
        help_text="Seleccione el tipo de documento del catálogo"
    )
    archivo = models.FileField(
        upload_to='documentos_trabajadores/%Y/%m/',
        verbose_name="Archivo",
        help_text="Archivo PDF, imagen (JPG, PNG) u otro formato"
    )
    nombre_archivo_original = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Nombre del archivo original",
        help_text="Se guarda automáticamente al subir el archivo"
    )
    fecha_carga = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de carga"
    )
    vigencia_desde = models.DateField(
        blank=True,
        null=True,
        verbose_name="Vigente desde",
        help_text="Fecha de inicio de vigencia (opcional)"
    )
    vigencia_hasta = models.DateField(
        blank=True,
        null=True,
        verbose_name="Vigente hasta",
        help_text="Fecha de vencimiento del documento (opcional)"
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones",
        help_text="Notas adicionales sobre el documento"
    )
    cargado_por = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Cargado por",
        help_text="Usuario que cargó el documento"
    )

    class Meta:
        db_table = 'trabajadores_documentos'
        verbose_name = 'Documento del Trabajador'
        verbose_name_plural = 'Documentos de Trabajadores'
        ordering = ['-fecha_carga']

    def __str__(self):
        return f"{self.tipo_documento.nombre_tipo_documento} - {self.id_trabajador.nombres} {self.id_trabajador.apellidos}"

    def save(self, *args, **kwargs):
        # Guardar el nombre original del archivo
        if self.archivo and not self.nombre_archivo_original:
            self.nombre_archivo_original = self.archivo.name
        super().save(*args, **kwargs)

    def get_extension(self):
        """Retorna la extensión del archivo"""
        import os
        if self.archivo:
            return os.path.splitext(self.archivo.name)[1].lower()
        return ''

    def es_imagen(self):
        """Verifica si el archivo es una imagen"""
        extensiones_imagen = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        return self.get_extension() in extensiones_imagen

    def es_pdf(self):
        """Verifica si el archivo es un PDF"""
        return self.get_extension() == '.pdf'

    def get_icono_tipo(self):
        """Retorna el icono de Bootstrap según el tipo de archivo"""
        ext = self.get_extension()
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
            return 'bi-file-earmark-image'
        elif ext == '.pdf':
            return 'bi-file-earmark-pdf'
        elif ext in ['.doc', '.docx']:
            return 'bi-file-earmark-word'
        elif ext in ['.xls', '.xlsx']:
            return 'bi-file-earmark-excel'
        else:
            return 'bi-file-earmark'

    def get_color_tipo(self):
        """Retorna el color Bootstrap según el tipo de archivo"""
        ext = self.get_extension()
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
            return 'primary'
        elif ext == '.pdf':
            return 'danger'
        elif ext in ['.doc', '.docx']:
            return 'info'
        elif ext in ['.xls', '.xlsx']:
            return 'success'
        else:
            return 'secondary'

    def esta_vigente(self):
        """Verifica si el documento está vigente (si tiene control de vigencia)"""
        if not self.tipo_documento.requiere_vigencia:
            return None  # No aplica control de vigencia
        
        if not self.vigencia_hasta:
            return None  # No tiene fecha configurada
        
        from datetime import date
        return date.today() <= self.vigencia_hasta

    def dias_para_vencer(self):
        """Retorna los días restantes para que venza el documento"""
        if not self.tipo_documento.requiere_vigencia or not self.vigencia_hasta:
            return None
        
        from datetime import date
        delta = self.vigencia_hasta - date.today()
        return delta.days

    def get_estado_vigencia(self):
        """Retorna el estado de vigencia del documento"""
        if not self.tipo_documento.requiere_vigencia:
            return 'sin_control'
        
        dias = self.dias_para_vencer()
        if dias is None:
            return 'sin_configurar'
        elif dias < 0:
            return 'vencido'
        elif dias <= 30:
            return 'proximo_vencer'
        else:
            return 'vigente'

    def get_color_vigencia(self):
        """Retorna el color Bootstrap según el estado de vigencia"""
        estado = self.get_estado_vigencia()
        colores = {
            'vigente': 'success',
            'proximo_vencer': 'warning',
            'vencido': 'danger',
            'sin_control': 'secondary',
            'sin_configurar': 'secondary'
        }
        return colores.get(estado, 'secondary')

    def get_tamano_archivo(self):
        """
        Retorna el tamaño del archivo en formato legible.
        Maneja archivos faltantes sin romper la aplicación.
        """
        if not self.archivo:
            return "Sin archivo"
        
        try:
            # Verificar si el archivo existe físicamente
            if not self.archivo.storage.exists(self.archivo.name):
                return "⚠️ Archivo no encontrado"
            
            # Si existe, obtener el tamaño
            size = self.archivo.size
            
            # Formatear el tamaño
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        
        except Exception as e:
            # Si hay cualquier error, retornar mensaje seguro
            return "⚠️ Error al leer archivo"
    
    def archivo_existe(self):
        """
        Verifica si el archivo existe físicamente.
        Útil para templates y vistas.
        """
        if not self.archivo:
            return False
        
        try:
            return self.archivo.storage.exists(self.archivo.name)
        except Exception:
            return False
    
    def get_url_archivo_segura(self):
        """
        Retorna la URL del archivo solo si existe.
        Retorna None si no existe para evitar links rotos.
        """
        if self.archivo_existe():
            try:
                return self.archivo.url
            except Exception:
                return None
        return None