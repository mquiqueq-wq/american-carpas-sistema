from django.db import models
from django.core.validators import MinValueValidator


# =====================================================
# MODELOS DE CATÁLOGO - FASE 1
# =====================================================


class TipoProveedor(models.Model):
    """
    Catálogo de tipos de proveedores
    Ejemplos: FABRICANTE, DISTRIBUIDOR, IMPORTADOR, MAYORISTA, SERVICIOS
    """
    id_tipo_proveedor = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre del tipo",
        help_text="Ej: Fabricante, Distribuidor, Importador"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción",
        help_text="Descripción detallada del tipo de proveedor"
    )
    requiere_certificaciones = models.BooleanField(
        default=False,
        verbose_name="¿Requiere certificaciones especiales?",
        help_text="Indica si este tipo de proveedor debe tener certificaciones específicas"
    )
    icono_bootstrap = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Icono Bootstrap",
        help_text="Ej: bi-building, bi-truck, bi-globe"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Si está activo, aparecerá disponible para asignar"
    )
    orden_visualizacion = models.IntegerField(
        default=0,
        verbose_name="Orden de visualización",
        help_text="Orden en que se muestra en listados (menor = primero)"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tipos_proveedores'
        verbose_name = 'Tipo de Proveedor'
        verbose_name_plural = 'Tipos de Proveedores'
        ordering = ['orden_visualizacion', 'nombre_tipo']

    def __str__(self):
        return self.nombre_tipo

    def count_proveedores_activos(self):
        """Retorna la cantidad de proveedores activos de este tipo"""
        return self.proveedores.filter(estado='ACTIVO').count()


class CategoriaProveedor(models.Model):
    """
    Catálogo de categorías de proveedores (productos/servicios que ofrecen)
    Ejemplos: LONAS Y TELAS, ESTRUCTURAS METÁLICAS, HERRAJES, TRANSPORTE
    """
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre de la categoría",
        help_text="Ej: Lonas y Telas, Estructuras Metálicas"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción",
        help_text="Descripción de los productos/servicios de esta categoría"
    )
    categoria_padre = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='subcategorias',
        verbose_name="Categoría padre",
        help_text="Para crear jerarquía de categorías (opcional)"
    )
    color_badge = models.CharField(
        max_length=20,
        default='primary',
        verbose_name="Color del badge",
        help_text="Color Bootstrap: primary, success, danger, warning, info, secondary"
    )
    icono_bootstrap = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Icono Bootstrap",
        help_text="Ej: bi-basket, bi-box, bi-tools"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Si está activo, aparecerá disponible para asignar"
    )
    orden_visualizacion = models.IntegerField(
        default=0,
        verbose_name="Orden de visualización",
        help_text="Orden en que se muestra en listados (menor = primero)"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categorias_proveedores'
        verbose_name = 'Categoría de Proveedor'
        verbose_name_plural = 'Categorías de Proveedores'
        ordering = ['orden_visualizacion', 'nombre_categoria']

    def __str__(self):
        if self.categoria_padre:
            return f"{self.categoria_padre.nombre_categoria} > {self.nombre_categoria}"
        return self.nombre_categoria

    def count_proveedores_activos(self):
        """Retorna la cantidad de proveedores activos de esta categoría"""
        return self.proveedores_categoria_principal.filter(estado='ACTIVO').count()

    def get_subcategorias(self):
        """Retorna las subcategorías de esta categoría"""
        return self.subcategorias.filter(activo=True)

    def tiene_subcategorias(self):
        """Verifica si tiene subcategorías"""
        return self.subcategorias.filter(activo=True).exists()


class TipoDocumentoProveedor(models.Model):
    """
    Catálogo de tipos de documentos que deben tener los proveedores
    Ejemplos: RUT, Cámara de Comercio, Certificación Bancaria, ISO 9001
    """
    id_tipo_documento = models.AutoField(primary_key=True)
    nombre_tipo_documento = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre del tipo de documento",
        help_text="Ej: RUT, Cámara de Comercio, Certificado ISO"
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
        help_text="Indica si este documento es obligatorio para todos los proveedores"
    )
    requiere_vigencia = models.BooleanField(
        default=False,
        verbose_name="¿Requiere control de vigencia?",
        help_text="Indica si el documento tiene fecha de vencimiento"
    )
    dias_alerta_vencimiento = models.IntegerField(
        default=30,
        validators=[MinValueValidator(1)],
        verbose_name="Días de alerta antes del vencimiento",
        help_text="Días antes del vencimiento para generar alerta"
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
        help_text="Orden en que se muestra en el detalle del proveedor (menor = primero)"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Si está activo, aparecerá disponible para asignar"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tipos_documentos_proveedores'
        verbose_name = 'Tipo de Documento de Proveedor'
        verbose_name_plural = 'Tipos de Documentos de Proveedores'
        ordering = ['orden_visualizacion', 'nombre_tipo_documento']

    def __str__(self):
        return self.nombre_tipo_documento

    def count_documentos_activos(self):
        """Retorna la cantidad de documentos activos de este tipo"""
        return self.documentos_proveedores.count()


# =====================================================
# MODELO PRINCIPAL - FASE 2
# =====================================================

# Choices para el modelo Proveedor
TIPO_DOCUMENTO_CHOICES = [
    ('NIT', 'NIT'),
    ('RUT', 'RUT'),
    ('CC', 'Cédula de Ciudadanía'),
    ('CE', 'Cédula de Extranjería'),
    ('PASAPORTE', 'Pasaporte'),
]

REGIMEN_TRIBUTARIO_CHOICES = [
    ('COMUN', 'Régimen Común'),
    ('SIMPLIFICADO', 'Régimen Simplificado'),
    ('GRAN_CONTRIBUYENTE', 'Gran Contribuyente'),
]

RESPONSABILIDAD_FISCAL_CHOICES = [
    ('IVA', 'Responsable de IVA'),
    ('NO_IVA', 'No responsable de IVA'),
    ('RETENEDOR', 'Agente de retención'),
]

TIPO_CUENTA_CHOICES = [
    ('AHORROS', 'Ahorros'),
    ('CORRIENTE', 'Corriente'),
]

ESTADO_PROVEEDOR_CHOICES = [
    ('ACTIVO', 'Activo'),
    ('INACTIVO', 'Inactivo'),
    ('BLOQUEADO', 'Bloqueado'),
    ('EN_EVALUACION', 'En evaluación'),
]


class Proveedor(models.Model):
    """
    Modelo principal de Proveedor con información completa
    """
    # ===== IDENTIFICACIÓN BÁSICA =====
    id_proveedor = models.AutoField(primary_key=True)
    
    razon_social = models.CharField(
        max_length=200,
        verbose_name="Razón Social",
        help_text="Nombre legal de la empresa"
    )
    
    nombre_comercial = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Nombre Comercial",
        help_text="Nombre con el que se conoce comercialmente"
    )
    
    tipo_documento = models.CharField(
        max_length=20,
        choices=TIPO_DOCUMENTO_CHOICES,
        default='NIT',
        verbose_name="Tipo de Documento"
    )
    
    numero_documento = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Número de Documento",
        help_text="NIT, RUT o documento de identificación"
    )
    
    digito_verificacion = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Dígito de Verificación",
        help_text="Solo para NIT"
    )
    
    tipo_proveedor = models.ForeignKey(
        TipoProveedor,
        on_delete=models.PROTECT,
        related_name='proveedores',
        verbose_name="Tipo de Proveedor"
    )
    
    categoria_principal = models.ForeignKey(
        CategoriaProveedor,
        on_delete=models.PROTECT,
        related_name='proveedores_categoria_principal',
        verbose_name="Categoría Principal"
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_PROVEEDOR_CHOICES,
        default='ACTIVO',
        verbose_name="Estado"
    )
    
    # ===== INFORMACIÓN LEGAL Y TRIBUTARIA =====
    regimen_tributario = models.CharField(
        max_length=30,
        choices=REGIMEN_TRIBUTARIO_CHOICES,
        default='COMUN',
        verbose_name="Régimen Tributario"
    )
    
    responsabilidad_fiscal = models.CharField(
        max_length=20,
        choices=RESPONSABILIDAD_FISCAL_CHOICES,
        default='IVA',
        verbose_name="Responsabilidad Fiscal"
    )
    
    actividad_economica = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Actividad Económica",
        help_text="Descripción de la actividad principal"
    )
    
    codigo_ciiu = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Código CIIU",
        help_text="Código de clasificación industrial"
    )
    
    pais_origen = models.CharField(
        max_length=50,
        default='Colombia',
        verbose_name="País de Origen"
    )
    
    # ===== INFORMACIÓN DE CONTACTO =====
    direccion_principal = models.CharField(
        max_length=200,
        verbose_name="Dirección Principal"
    )
    
    ciudad = models.CharField(
        max_length=100,
        verbose_name="Ciudad"
    )
    
    departamento = models.CharField(
        max_length=100,
        verbose_name="Departamento"
    )
    
    pais = models.CharField(
        max_length=50,
        default='Colombia',
        verbose_name="País"
    )
    
    codigo_postal = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Código Postal"
    )
    
    telefono_principal = models.CharField(
        max_length=20,
        verbose_name="Teléfono Principal"
    )
    
    telefono_secundario = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Teléfono Secundario"
    )
    
    email_principal = models.EmailField(
        verbose_name="Email Principal"
    )
    
    email_facturacion = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email de Facturación",
        help_text="Email para envío de facturas"
    )
    
    sitio_web = models.URLField(
        blank=True,
        null=True,
        verbose_name="Sitio Web"
    )
    
    horario_atencion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Horario de Atención",
        help_text="Ej: Lunes a Viernes 8:00 AM - 5:00 PM"
    )
    
    # ===== INFORMACIÓN BANCARIA =====
    banco = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Banco"
    )
    
    tipo_cuenta = models.CharField(
        max_length=20,
        choices=TIPO_CUENTA_CHOICES,
        blank=True,
        null=True,
        verbose_name="Tipo de Cuenta"
    )
    
    numero_cuenta = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Número de Cuenta"
    )
    
    titular_cuenta = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Titular de la Cuenta"
    )
    
    # ===== CONDICIONES COMERCIALES =====
    plazo_entrega_dias = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Plazo de Entrega (días)",
        help_text="Días promedio de entrega"
    )
    
    tiempo_credito_dias = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Tiempo de Crédito (días)",
        help_text="Días de crédito que ofrece"
    )
    
    descuento_pronto_pago = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Descuento Pronto Pago (%)",
        help_text="Porcentaje de descuento por pronto pago"
    )
    
    monto_minimo_pedido = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        verbose_name="Monto Mínimo de Pedido",
        help_text="Valor mínimo de compra"
    )
    
    acepta_credito = models.BooleanField(
        default=False,
        verbose_name="¿Acepta Crédito?",
        help_text="Si el proveedor maneja ventas a crédito"
    )
    
    metodos_pago_aceptados = models.TextField(
        blank=True,
        null=True,
        verbose_name="Métodos de Pago Aceptados",
        help_text="Ej: Efectivo, Transferencia, Cheque, Tarjeta"
    )
    
    # ===== CONTROL Y SEGUIMIENTO =====
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )
    
    fecha_ultima_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Modificación"
    )
    
    fecha_ultima_compra = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de Última Compra"
    )
    
    total_compras_historico = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Total Compras Histórico",
        help_text="Suma total de todas las compras realizadas"
    )
    
    calificacion_promedio = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        verbose_name="Calificación Promedio",
        help_text="Calificación promedio (0-5)"
    )
    
    numero_evaluaciones = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Número de Evaluaciones"
    )
    
    registrado_por = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Registrado Por",
        help_text="Usuario que registró el proveedor"
    )
    
    observaciones_generales = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones Generales"
    )
    
    class Meta:
        db_table = 'proveedores'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['razon_social']
    
    def __str__(self):
        return f"{self.razon_social} ({self.numero_documento})"
    
    def get_nombre_completo(self):
        """Retorna el nombre comercial si existe, sino la razón social"""
        return self.nombre_comercial if self.nombre_comercial else self.razon_social
    
    def get_documento_completo(self):
        """Retorna el documento con dígito de verificación si aplica"""
        if self.digito_verificacion:
            return f"{self.numero_documento}-{self.digito_verificacion}"
        return self.numero_documento
    
    def get_direccion_completa(self):
        """Retorna la dirección completa formateada"""
        return f"{self.direccion_principal}, {self.ciudad}, {self.departamento}, {self.pais}"
    
    def get_estado_badge_class(self):
        """Retorna la clase CSS para el badge de estado"""
        estados = {
            'ACTIVO': 'bg-success',
            'INACTIVO': 'bg-secondary',
            'BLOQUEADO': 'bg-danger',
            'EN_EVALUACION': 'bg-warning'
        }
        return estados.get(self.estado, 'bg-secondary')
    
    def tiene_informacion_completa(self):
        """Verifica si el proveedor tiene toda la información básica completa"""
        campos_requeridos = [
            self.razon_social,
            self.numero_documento,
            self.direccion_principal,
            self.ciudad,
            self.telefono_principal,
            self.email_principal
        ]
        return all(campos_requeridos)


# =====================================================
# MODELO DE CONTACTOS - FASE 3
# =====================================================

# Choices para ContactoProveedor
AREA_RESPONSABILIDAD_CHOICES = [
    ('VENTAS', 'Ventas'),
    ('COMPRAS', 'Compras'),
    ('FACTURACION', 'Facturación'),
    ('TECNICO', 'Técnico'),
    ('LOGISTICA', 'Logística'),
    ('GERENCIA', 'Gerencia'),
    ('OTRO', 'Otro'),
]


class ContactoProveedor(models.Model):
    """
    Modelo para gestionar múltiples contactos por proveedor
    """
    id_contacto = models.AutoField(primary_key=True)
    
    id_proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name='contactos',
        verbose_name="Proveedor"
    )
    
    nombre_completo = models.CharField(
        max_length=200,
        verbose_name="Nombre Completo"
    )
    
    cargo = models.CharField(
        max_length=100,
        verbose_name="Cargo",
        help_text="Ej: Gerente de Ventas, Coordinador de Logística"
    )
    
    departamento = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Departamento",
        help_text="Ej: Ventas, Producción, Administración"
    )
    
    area_responsabilidad = models.CharField(
        max_length=20,
        choices=AREA_RESPONSABILIDAD_CHOICES,
        default='VENTAS',
        verbose_name="Área de Responsabilidad"
    )
    
    telefono_directo = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Teléfono Directo",
        help_text="Extensión o línea directa (opcional)"
    )
    
    telefono_celular = models.CharField(
        max_length=20,
        verbose_name="Teléfono Celular"
    )
    
    email = models.EmailField(
        verbose_name="Email"
    )
    
    es_contacto_principal = models.BooleanField(
        default=False,
        verbose_name="¿Es contacto principal?",
        help_text="Solo puede haber un contacto principal por proveedor"
    )
    
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones",
        help_text="Notas adicionales sobre el contacto"
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Modificación"
    )
    
    class Meta:
        db_table = 'contactos_proveedores'
        verbose_name = 'Contacto de Proveedor'
        verbose_name_plural = 'Contactos de Proveedores'
        ordering = ['-es_contacto_principal', 'nombre_completo']
    
    def __str__(self):
        return f"{self.nombre_completo} - {self.cargo} ({self.id_proveedor.razon_social})"
    
    def save(self, *args, **kwargs):
        """
        Validar que solo haya un contacto principal por proveedor
        """
        if self.es_contacto_principal:
            # Quitar el flag de principal a otros contactos del mismo proveedor
            ContactoProveedor.objects.filter(
                id_proveedor=self.id_proveedor,
                es_contacto_principal=True
            ).exclude(id_contacto=self.id_contacto).update(es_contacto_principal=False)
        
        super().save(*args, **kwargs)
    
    def get_telefono_completo(self):
        """Retorna teléfono con extensión si existe"""
        if self.telefono_directo:
            return f"{self.telefono_celular} / Ext: {self.telefono_directo}"
        return self.telefono_celular
