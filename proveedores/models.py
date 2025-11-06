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
