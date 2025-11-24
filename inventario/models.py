"""
Modelos para el módulo de Inventario de Carpas
American Carpas 1 SAS

Este módulo gestiona:
- Inventario de Lonas (rollos con control de metraje)
- Inventario de Estructura (tubería con control de metros/piezas)
- Inventario de Accesorios (tensores, estacas, cortinas, etc.)
- Órdenes de Producción (fabricación de carpas)
- Historial de Movimientos (trazabilidad completa)

Autor: Mario - Universidad La Gran Colombia
Versión: 2.0 - Modelo Unificado
Fecha: Noviembre 2025
"""

import uuid
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone


# =============================================================================
# CATÁLOGOS BASE - UBICACIONES
# =============================================================================

class UbicacionAlmacen(models.Model):
    """
    Catálogo de ubicaciones físicas en el almacén.
    Ejemplo: Bodega A - Estante 3 - Nivel 2
    """
    id_ubicacion = models.AutoField(primary_key=True)
    codigo = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Código",
        help_text="Ej: BOD-A-E3-N2"
    )
    nombre = models.CharField(
        max_length=150,
        verbose_name="Nombre Completo",
        help_text="Ej: Bodega A - Estante 3 - Nivel 2"
    )
    bodega = models.CharField(
        max_length=50,
        verbose_name="Bodega",
        help_text="Ej: Bodega Principal, Bodega Secundaria"
    )
    zona = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Zona",
        help_text="Ej: Zona A, Zona de Lonas"
    )
    estante = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Estante"
    )
    nivel = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Nivel"
    )
    capacidad_descripcion = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Capacidad",
        help_text="Descripción de capacidad: Rollos grandes, Tubería larga, etc."
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Creación"
    )

    class Meta:
        db_table = 'inv_ubicacion_almacen'
        verbose_name = 'Ubicación de Almacén'
        verbose_name_plural = 'Ubicaciones de Almacén'
        ordering = ['bodega', 'zona', 'estante', 'nivel']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


# =============================================================================
# CATÁLOGOS - LONAS
# =============================================================================

class TipoLona(models.Model):
    """Catálogo de tipos de lona: PVC, Vinílica, Polietileno, etc."""
    id_tipo_lona = models.AutoField(primary_key=True)
    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código"
    )
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'inv_tipo_lona'
        verbose_name = 'Tipo de Lona'
        verbose_name_plural = 'Tipos de Lona'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class AnchoLona(models.Model):
    """Catálogo de anchos de lona en metros: 1.50m, 2.00m, 2.50m, etc."""
    id_ancho = models.AutoField(primary_key=True)
    valor_metros = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        unique=True,
        verbose_name="Ancho (metros)"
    )
    descripcion = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        db_table = 'inv_ancho_lona'
        verbose_name = 'Ancho de Lona'
        verbose_name_plural = 'Anchos de Lona'
        ordering = ['valor_metros']

    def __str__(self):
        return f"{self.valor_metros}m"


class ColorLona(models.Model):
    """Catálogo de colores de lona con código hexadecimal opcional."""
    id_color = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nombre del Color"
    )
    codigo_hex = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        verbose_name="Código Hexadecimal",
        help_text="Ej: #FFFFFF para blanco"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        db_table = 'inv_color_lona'
        verbose_name = 'Color de Lona'
        verbose_name_plural = 'Colores de Lona'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class TratamientoLona(models.Model):
    """Catálogo de tratamientos especiales: Impermeabilizado, Ignífugo, Anti-UV, etc."""
    id_tratamiento = models.AutoField(primary_key=True)
    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código"
    )
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        db_table = 'inv_tratamiento_lona'
        verbose_name = 'Tratamiento de Lona'
        verbose_name_plural = 'Tratamientos de Lona'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


# =============================================================================
# CATÁLOGOS - ESTRUCTURA
# =============================================================================

class TipoEstructura(models.Model):
    """Catálogo de tipos de estructura: Tubo redondo, Tubo cuadrado, Perfil, etc."""
    id_tipo_estructura = models.AutoField(primary_key=True)
    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código"
    )
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'inv_tipo_estructura'
        verbose_name = 'Tipo de Estructura'
        verbose_name_plural = 'Tipos de Estructura'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class MedidaTubo(models.Model):
    """Catálogo de medidas de tubo: 1", 1½", 2", 2½", etc."""
    id_medida = models.AutoField(primary_key=True)
    valor_medida = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Medida",
        help_text="Ej: 1 pulgada, 1½ pulgadas, 2 pulgadas"
    )
    valor_pulgadas = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Valor en Pulgadas",
        help_text="Valor numérico para ordenamiento"
    )
    descripcion = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        db_table = 'inv_medida_tubo'
        verbose_name = 'Medida de Tubo'
        verbose_name_plural = 'Medidas de Tubo'
        ordering = ['valor_pulgadas', 'valor_medida']

    def __str__(self):
        return self.valor_medida


class Calibre(models.Model):
    """Catálogo de calibres de tubería: 14, 16, 18, 20, etc."""
    id_calibre = models.AutoField(primary_key=True)
    valor_calibre = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        unique=True,
        verbose_name="Calibre"
    )
    espesor_mm = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name="Espesor (mm)",
        help_text="Espesor equivalente en milímetros"
    )
    descripcion = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        db_table = 'inv_calibre'
        verbose_name = 'Calibre'
        verbose_name_plural = 'Calibres'
        ordering = ['valor_calibre']

    def __str__(self):
        return f"Calibre {self.valor_calibre}"


class MaterialEstructura(models.Model):
    """Catálogo de materiales: Acero galvanizado, Aluminio, Hierro negro, etc."""
    id_material = models.AutoField(primary_key=True)
    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código"
    )
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        db_table = 'inv_material_estructura'
        verbose_name = 'Material de Estructura'
        verbose_name_plural = 'Materiales de Estructura'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class AcabadoEstructura(models.Model):
    """Catálogo de acabados: Galvanizado en caliente, Pintura electrostática, etc."""
    id_acabado = models.AutoField(primary_key=True)
    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código"
    )
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        db_table = 'inv_acabado_estructura'
        verbose_name = 'Acabado de Estructura'
        verbose_name_plural = 'Acabados de Estructura'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


# =============================================================================
# CATÁLOGOS - ACCESORIOS
# =============================================================================

class TipoAccesorio(models.Model):
    """Catálogo de tipos de accesorios: Tensor, Estaca, Cuerda, Cortina, etc."""
    id_tipo_accesorio = models.AutoField(primary_key=True)
    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código",
        help_text="Ej: TEN, EST, CUE, COR"
    )
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    unidad_medida = models.CharField(
        max_length=20,
        default='unidad',
        verbose_name="Unidad de Medida",
        help_text="unidad, metro, rollo, par"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'inv_tipo_accesorio'
        verbose_name = 'Tipo de Accesorio'
        verbose_name_plural = 'Tipos de Accesorios'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


# =============================================================================
# INVENTARIO PRINCIPAL - LONAS
# =============================================================================

class InventarioLona(models.Model):
    """
    Inventario de rollos de lona con control de metraje.
    Cada registro representa un rollo físico con su trazabilidad.
    """
    
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('EN_USO', 'En Uso'),
        ('RESERVADO', 'Reservado'),
        ('AGOTADO', 'Agotado'),
        ('BAJA', 'Dado de Baja'),
    ]
    
    id_lona = models.AutoField(primary_key=True)
    
    # Identificación
    codigo_rollo = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Código del Rollo",
        help_text="Autogenerado: LON-0001"
    )
    codigo_qr = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name="Código QR (UUID)"
    )
    
    # Características (FKs a catálogos)
    tipo_lona = models.ForeignKey(
        TipoLona,
        on_delete=models.PROTECT,
        related_name='inventario_lonas',
        verbose_name="Tipo de Lona"
    )
    ancho_lona = models.ForeignKey(
        AnchoLona,
        on_delete=models.PROTECT,
        related_name='inventario_lonas',
        verbose_name="Ancho"
    )
    color_lona = models.ForeignKey(
        ColorLona,
        on_delete=models.PROTECT,
        related_name='inventario_lonas',
        verbose_name="Color"
    )
    tratamiento = models.ForeignKey(
        TratamientoLona,
        on_delete=models.PROTECT,
        related_name='inventario_lonas',
        blank=True,
        null=True,
        verbose_name="Tratamiento"
    )
    gramaje = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Gramaje (g/m²)",
        help_text="Peso en gramos por metro cuadrado"
    )
    
    # Control de Metraje
    metros_iniciales = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Metros Iniciales",
        help_text="Metros totales al recibir el rollo"
    )
    metros_disponibles = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Metros Disponibles"
    )
    metros_reservados = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Metros Reservados",
        help_text="Metros reservados para órdenes pendientes"
    )
    metros_minimo_alerta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=10,
        verbose_name="Stock Mínimo (metros)",
        help_text="Genera alerta cuando llegue a este nivel"
    )
    
    # Costos
    costo_por_metro = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Costo por Metro"
    )
    
    # Ubicación y Origen
    ubicacion = models.ForeignKey(
        UbicacionAlmacen,
        on_delete=models.PROTECT,
        related_name='lonas',
        verbose_name="Ubicación en Almacén"
    )
    proveedor = models.ForeignKey(
        'proveedores.Proveedor',
        on_delete=models.SET_NULL,
        related_name='lonas_suministradas',
        blank=True,
        null=True,
        verbose_name="Proveedor"
    )
    lote_serial = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Lote/Serial del Proveedor"
    )
    numero_factura = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Número de Factura"
    )
    
    # Fechas
    fecha_ingreso = models.DateField(
        verbose_name="Fecha de Ingreso"
    )
    fecha_fabricacion = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de Fabricación"
    )
    fecha_ultima_salida = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha Última Salida"
    )
    garantia_meses = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Garantía (meses)"
    )
    
    # Estado y Control
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='DISPONIBLE',
        verbose_name="Estado"
    )
    imagen = models.ImageField(
        upload_to='inventario/lonas/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Imagen"
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    # Auditoría
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='lonas_creadas',
        blank=True,
        null=True,
        verbose_name="Creado Por"
    )
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )

    class Meta:
        db_table = 'inv_inventario_lona'
        verbose_name = 'Inventario de Lona'
        verbose_name_plural = 'Inventario de Lonas'
        ordering = ['-fecha_ingreso', 'tipo_lona']

    def __str__(self):
        return f"{self.codigo_rollo} - {self.tipo_lona} {self.ancho_lona} {self.color_lona}"

    def save(self, *args, **kwargs):
        # Generar código si no existe
        if not self.codigo_rollo:
            self.codigo_rollo = self._generar_codigo()
        
        # Actualizar estado según metros
        if self.metros_disponibles <= 0:
            self.estado = 'AGOTADO'
        elif self.metros_disponibles <= self.metros_minimo_alerta and self.estado == 'DISPONIBLE':
            pass  # Mantener disponible pero se generará alerta
        
        super().save(*args, **kwargs)

    def _generar_codigo(self):
        """Genera código único para el rollo"""
        ultimo = InventarioLona.objects.order_by('-id_lona').first()
        nuevo_num = (ultimo.id_lona + 1) if ultimo else 1
        return f"LON-{nuevo_num:04d}"

    @property
    def metros_utilizados(self):
        """Metros ya utilizados del rollo"""
        return self.metros_iniciales - self.metros_disponibles

    @property
    def metros_reales_disponibles(self):
        """Metros disponibles menos reservados"""
        return self.metros_disponibles - self.metros_reservados

    @property
    def valor_inventario(self):
        """Valor actual del inventario"""
        return self.metros_disponibles * self.costo_por_metro

    @property
    def porcentaje_disponible(self):
        """Porcentaje de metros disponibles"""
        if self.metros_iniciales <= 0:
            return 0
        return round((self.metros_disponibles / self.metros_iniciales) * 100, 2)

    def en_stock_minimo(self):
        """Verifica si está en stock mínimo"""
        return self.metros_disponibles <= self.metros_minimo_alerta


# =============================================================================
# INVENTARIO PRINCIPAL - ESTRUCTURA
# =============================================================================

class InventarioEstructura(models.Model):
    """
    Inventario de estructura/tubería con control de metros lineales o piezas.
    """
    
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('EN_USO', 'En Uso'),
        ('RESERVADO', 'Reservado'),
        ('AGOTADO', 'Agotado'),
        ('BAJA', 'Dado de Baja'),
    ]
    
    CONTROL_CHOICES = [
        ('METROS', 'Por Metros Lineales'),
        ('PIEZAS', 'Por Piezas/Unidades'),
    ]
    
    id_estructura = models.AutoField(primary_key=True)
    
    # Identificación
    codigo_lote = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Código del Lote",
        help_text="Autogenerado: EST-0001"
    )
    codigo_qr = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name="Código QR (UUID)"
    )
    
    # Características
    tipo_estructura = models.ForeignKey(
        TipoEstructura,
        on_delete=models.PROTECT,
        related_name='inventario_estructuras',
        verbose_name="Tipo de Estructura"
    )
    medida_tubo = models.ForeignKey(
        MedidaTubo,
        on_delete=models.PROTECT,
        related_name='inventario_estructuras',
        verbose_name="Medida del Tubo"
    )
    calibre = models.ForeignKey(
        Calibre,
        on_delete=models.PROTECT,
        related_name='inventario_estructuras',
        verbose_name="Calibre"
    )
    material = models.ForeignKey(
        MaterialEstructura,
        on_delete=models.PROTECT,
        related_name='inventario_estructuras',
        blank=True,
        null=True,
        verbose_name="Material"
    )
    acabado = models.ForeignKey(
        AcabadoEstructura,
        on_delete=models.PROTECT,
        related_name='inventario_estructuras',
        blank=True,
        null=True,
        verbose_name="Acabado"
    )
    peso_por_metro = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name="Peso por Metro (kg)",
        help_text="Kilogramos por metro lineal"
    )
    
    # Tipo de Control
    tipo_control = models.CharField(
        max_length=10,
        choices=CONTROL_CHOICES,
        default='METROS',
        verbose_name="Tipo de Control",
        help_text="Controlar por metros lineales o por piezas"
    )
    
    # Control por Metros
    metros_iniciales = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Metros Iniciales"
    )
    metros_disponibles = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Metros Disponibles"
    )
    metros_reservados = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Metros Reservados"
    )
    metros_minimo_alerta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=10,
        verbose_name="Stock Mínimo (metros)"
    )
    
    # Control por Piezas
    longitud_pieza = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Longitud por Pieza (m)",
        help_text="Si son tubos cortados, longitud de cada pieza"
    )
    piezas_iniciales = models.PositiveIntegerField(
        default=0,
        verbose_name="Piezas Iniciales"
    )
    piezas_disponibles = models.PositiveIntegerField(
        default=0,
        verbose_name="Piezas Disponibles"
    )
    piezas_reservadas = models.PositiveIntegerField(
        default=0,
        verbose_name="Piezas Reservadas"
    )
    piezas_minimo_alerta = models.PositiveIntegerField(
        default=5,
        verbose_name="Stock Mínimo (piezas)"
    )
    
    # Costos
    costo_por_metro = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Costo por Metro"
    )
    costo_por_pieza = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Costo por Pieza"
    )
    
    # Ubicación y Origen
    ubicacion = models.ForeignKey(
        UbicacionAlmacen,
        on_delete=models.PROTECT,
        related_name='estructuras',
        verbose_name="Ubicación en Almacén"
    )
    proveedor = models.ForeignKey(
        'proveedores.Proveedor',
        on_delete=models.SET_NULL,
        related_name='estructuras_suministradas',
        blank=True,
        null=True,
        verbose_name="Proveedor"
    )
    lote_serial = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Lote/Serial del Proveedor"
    )
    numero_factura = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Número de Factura"
    )
    
    # Fechas
    fecha_ingreso = models.DateField(
        verbose_name="Fecha de Ingreso"
    )
    fecha_ultima_salida = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha Última Salida"
    )
    
    # Estado y Control
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='DISPONIBLE',
        verbose_name="Estado"
    )
    imagen = models.ImageField(
        upload_to='inventario/estructura/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Imagen"
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    # Auditoría
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='estructuras_creadas',
        blank=True,
        null=True,
        verbose_name="Creado Por"
    )
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )

    class Meta:
        db_table = 'inv_inventario_estructura'
        verbose_name = 'Inventario de Estructura'
        verbose_name_plural = 'Inventario de Estructuras'
        ordering = ['-fecha_ingreso', 'tipo_estructura']

    def __str__(self):
        return f"{self.codigo_lote} - {self.tipo_estructura} {self.medida_tubo} Cal.{self.calibre.valor_calibre}"

    def save(self, *args, **kwargs):
        if not self.codigo_lote:
            self.codigo_lote = self._generar_codigo()
        
        # Actualizar estado
        if self.tipo_control == 'METROS' and self.metros_disponibles <= 0:
            self.estado = 'AGOTADO'
        elif self.tipo_control == 'PIEZAS' and self.piezas_disponibles <= 0:
            self.estado = 'AGOTADO'
        
        super().save(*args, **kwargs)

    def _generar_codigo(self):
        ultimo = InventarioEstructura.objects.order_by('-id_estructura').first()
        nuevo_num = (ultimo.id_estructura + 1) if ultimo else 1
        return f"EST-{nuevo_num:04d}"

    @property
    def valor_inventario(self):
        if self.tipo_control == 'METROS':
            return self.metros_disponibles * self.costo_por_metro
        return self.piezas_disponibles * self.costo_por_pieza


# =============================================================================
# INVENTARIO PRINCIPAL - ACCESORIOS
# =============================================================================

class InventarioAccesorio(models.Model):
    """
    Inventario de accesorios para carpas: tensores, estacas, cuerdas, cortinas, etc.
    """
    
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('EN_USO', 'En Uso'),
        ('RESERVADO', 'Reservado'),
        ('AGOTADO', 'Agotado'),
        ('BAJA', 'Dado de Baja'),
    ]
    
    id_accesorio = models.AutoField(primary_key=True)
    
    # Identificación
    codigo = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Código",
        help_text="Autogenerado: ACC-0001"
    )
    codigo_qr = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name="Código QR (UUID)"
    )
    
    # Características
    tipo_accesorio = models.ForeignKey(
        TipoAccesorio,
        on_delete=models.PROTECT,
        related_name='inventario_accesorios',
        verbose_name="Tipo de Accesorio"
    )
    nombre = models.CharField(
        max_length=150,
        verbose_name="Nombre",
        help_text="Ej: Tensor galvanizado 1/2 pulgada"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    especificaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Especificaciones",
        help_text="Material, dimensiones, etc."
    )
    
    # Control de Cantidad
    cantidad_inicial = models.PositiveIntegerField(
        verbose_name="Cantidad Inicial"
    )
    cantidad_disponible = models.PositiveIntegerField(
        verbose_name="Cantidad Disponible"
    )
    cantidad_reservada = models.PositiveIntegerField(
        default=0,
        verbose_name="Cantidad Reservada"
    )
    cantidad_minima_alerta = models.PositiveIntegerField(
        default=5,
        verbose_name="Stock Mínimo"
    )
    
    # Costos
    costo_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Costo Unitario"
    )
    
    # Ubicación y Origen
    ubicacion = models.ForeignKey(
        UbicacionAlmacen,
        on_delete=models.PROTECT,
        related_name='accesorios',
        verbose_name="Ubicación en Almacén"
    )
    proveedor = models.ForeignKey(
        'proveedores.Proveedor',
        on_delete=models.SET_NULL,
        related_name='accesorios_suministrados',
        blank=True,
        null=True,
        verbose_name="Proveedor"
    )
    lote_serial = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Lote/Serial"
    )
    
    # Fechas
    fecha_ingreso = models.DateField(
        verbose_name="Fecha de Ingreso"
    )
    fecha_ultima_salida = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha Última Salida"
    )
    
    # Estado y Control
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='DISPONIBLE',
        verbose_name="Estado"
    )
    imagen = models.ImageField(
        upload_to='inventario/accesorios/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Imagen"
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    # Auditoría
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='accesorios_creados',
        blank=True,
        null=True,
        verbose_name="Creado Por"
    )
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )

    class Meta:
        db_table = 'inv_inventario_accesorio'
        verbose_name = 'Inventario de Accesorio'
        verbose_name_plural = 'Inventario de Accesorios'
        ordering = ['tipo_accesorio', 'nombre']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self._generar_codigo()
        
        if self.cantidad_disponible <= 0:
            self.estado = 'AGOTADO'
        
        super().save(*args, **kwargs)

    def _generar_codigo(self):
        ultimo = InventarioAccesorio.objects.order_by('-id_accesorio').first()
        nuevo_num = (ultimo.id_accesorio + 1) if ultimo else 1
        return f"ACC-{nuevo_num:04d}"

    @property
    def valor_inventario(self):
        return self.cantidad_disponible * self.costo_unitario


# =============================================================================
# ÓRDENES DE PRODUCCIÓN
# =============================================================================

class OrdenProduccion(models.Model):
    """
    Orden de producción unificada para fabricación de carpas.
    Controla lonas, estructura y accesorios en una sola orden.
    """
    
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('PENDIENTE', 'Pendiente Autorización'),
        ('AUTORIZADA', 'Autorizada'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    PRIORIDAD_CHOICES = [
        (1, '1 - Muy Alta'),
        (2, '2 - Alta'),
        (3, '3 - Normal'),
        (4, '4 - Baja'),
        (5, '5 - Muy Baja'),
    ]
    
    id_orden = models.AutoField(primary_key=True)
    
    # Identificación
    numero_orden = models.PositiveIntegerField(
        verbose_name="Número de Orden",
        help_text="Consecutivo anual: 1201, 1202, etc."
    )
    año = models.PositiveIntegerField(
        verbose_name="Año",
        help_text="Año de la orden"
    )
    
    # Información General
    fecha_orden = models.DateField(
        default=timezone.now,
        verbose_name="Fecha de Orden"
    )
    fecha_entrega_requerida = models.DateField(
        verbose_name="Fecha de Entrega Requerida"
    )
    proyecto = models.ForeignKey(
        'proyectos.Proyecto',
        on_delete=models.SET_NULL,
        related_name='ordenes_produccion',
        blank=True,
        null=True,
        verbose_name="Proyecto Vinculado"
    )
    cliente = models.CharField(
        max_length=200,
        verbose_name="Cliente",
        help_text="Nombre del cliente o destino"
    )
    ubicacion_entrega = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Ubicación de Entrega"
    )
    
    # Control de Fases (como en el Excel)
    estructura_fabricada = models.BooleanField(
        default=False,
        verbose_name="Estructura Fabricada"
    )
    fecha_estructura_fabricada = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha Estructura Fabricada"
    )
    estructura_pintada = models.BooleanField(
        default=False,
        verbose_name="Estructura Pintada"
    )
    fecha_estructura_pintada = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha Estructura Pintada"
    )
    lona_fabricada = models.BooleanField(
        default=False,
        verbose_name="Lona Fabricada"
    )
    fecha_lona_fabricada = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha Lona Fabricada"
    )
    terminada = models.BooleanField(
        default=False,
        verbose_name="Terminada"
    )
    fecha_terminada = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha Terminada"
    )
    
    # Autorización (FK a Trabajadores)
    solicitado_por = models.ForeignKey(
        'trabajadores.TrabajadorPersonal',
        on_delete=models.PROTECT,
        related_name='ordenes_solicitadas',
        verbose_name="Solicitado Por"
    )
    autorizado_por = models.ForeignKey(
        'trabajadores.TrabajadorPersonal',
        on_delete=models.SET_NULL,
        related_name='ordenes_autorizadas',
        blank=True,
        null=True,
        verbose_name="Autorizado Por"
    )
    fecha_autorizacion = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Fecha de Autorización"
    )
    
    # Estado y Prioridad
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='BORRADOR',
        verbose_name="Estado"
    )
    es_urgente = models.BooleanField(
        default=False,
        verbose_name="Es Urgente"
    )
    prioridad = models.PositiveIntegerField(
        choices=PRIORIDAD_CHOICES,
        default=3,
        verbose_name="Prioridad"
    )
    
    # Fechas de Ejecución
    fecha_inicio_produccion = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha Inicio Producción"
    )
    fecha_fin_produccion = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha Fin Producción"
    )
    
    # Observaciones
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    # Auditoría
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='ordenes_creadas',
        blank=True,
        null=True,
        verbose_name="Creado Por"
    )
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )

    class Meta:
        db_table = 'inv_orden_produccion'
        verbose_name = 'Orden de Producción'
        verbose_name_plural = 'Órdenes de Producción'
        ordering = ['-año', '-numero_orden']
        unique_together = ['numero_orden', 'año']

    def __str__(self):
        return f"OP-{self.numero_orden} ({self.año})"

    def save(self, *args, **kwargs):
        # Asignar año si no existe
        if not self.año:
            self.año = timezone.now().year
        
        # Generar número de orden si es nuevo
        if not self.numero_orden:
            self.numero_orden = self._generar_numero_orden()
        
        super().save(*args, **kwargs)

    def _generar_numero_orden(self):
        """Genera el siguiente número de orden para el año actual"""
        ultimo = OrdenProduccion.objects.filter(
            año=self.año
        ).order_by('-numero_orden').first()
        
        if ultimo:
            return ultimo.numero_orden + 1
        return 1001  # Inicia en 1001 como en el Excel

    @property
    def codigo_completo(self):
        return f"OP-{self.numero_orden}-{self.año}"

    @property
    def porcentaje_avance(self):
        """Calcula el porcentaje de avance basado en las fases"""
        fases = [
            self.estructura_fabricada,
            self.estructura_pintada,
            self.lona_fabricada,
            self.terminada
        ]
        completadas = sum(1 for f in fases if f)
        return int((completadas / len(fases)) * 100)


class OrdenProduccionItem(models.Model):
    """
    Ítems/líneas de una orden de producción.
    Cada línea describe un producto a fabricar.
    """
    
    id_item = models.AutoField(primary_key=True)
    orden = models.ForeignKey(
        OrdenProduccion,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Orden de Producción"
    )
    numero_linea = models.PositiveIntegerField(
        verbose_name="# Línea"
    )
    
    # Descripción del Producto
    cantidad = models.PositiveIntegerField(
        default=1,
        verbose_name="Cantidad",
        help_text="Cantidad de carpas/productos"
    )
    tipo_producto = models.CharField(
        max_length=100,
        verbose_name="Tipo de Producto",
        help_text="CARPA TRADICIONAL, HANGAR, CUBIERTA, TARIMA, etc."
    )
    dimensiones = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Dimensiones",
        help_text="2x2 MTS, 10x20, 3x3MTS, etc."
    )
    color_estructura = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Color Estructura",
        help_text="NEGRA, GRIS, BLANCO, etc."
    )
    color_lona = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Color Lona",
        help_text="BLANCA, ESPAÑA, AZUL, etc."
    )
    
    # Accesorios Incluidos
    incluye_cortinas = models.BooleanField(
        default=False,
        verbose_name="Incluye Cortinas"
    )
    cantidad_cortinas = models.PositiveIntegerField(
        default=0,
        verbose_name="Cantidad Cortinas"
    )
    incluye_logo_techo = models.BooleanField(
        default=False,
        verbose_name="Logo en Techo"
    )
    cantidad_logos_techo = models.PositiveIntegerField(
        default=0,
        verbose_name="Cantidad Logos Techo"
    )
    incluye_logo_cortina = models.BooleanField(
        default=False,
        verbose_name="Logo en Cortina"
    )
    cantidad_logos_cortina = models.PositiveIntegerField(
        default=0,
        verbose_name="Cantidad Logos Cortina"
    )
    incluye_faldon = models.BooleanField(
        default=False,
        verbose_name="Incluye Faldón"
    )
    incluye_entecho = models.BooleanField(
        default=False,
        verbose_name="Incluye Entecho"
    )
    otros_accesorios = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="Otros Accesorios",
        help_text="2 ESCALERAS, FORRO, etc."
    )
    
    # Descripción Libre
    descripcion_completa = models.TextField(
        verbose_name="Descripción Completa",
        help_text="Descripción como aparece en el Excel"
    )
    especificaciones_cliente = models.TextField(
        blank=True,
        null=True,
        verbose_name="Especificaciones del Cliente",
        help_text="SEGÚN ESPECIFICACIONES DON ALBERTO, etc."
    )
    
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        db_table = 'inv_orden_produccion_item'
        verbose_name = 'Ítem de Orden'
        verbose_name_plural = 'Ítems de Orden'
        ordering = ['orden', 'numero_linea']
        unique_together = ['orden', 'numero_linea']

    def __str__(self):
        return f"{self.orden} - Línea {self.numero_linea}: {self.cantidad} {self.tipo_producto}"


# =============================================================================
# DETALLE DE MATERIALES POR ORDEN
# =============================================================================

class OrdenProduccionLona(models.Model):
    """
    Detalle de lonas utilizadas en una orden de producción.
    Registra qué rollos se usaron y quién hizo el corte.
    """
    
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CORTADO', 'Cortado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    id = models.AutoField(primary_key=True)
    orden = models.ForeignKey(
        OrdenProduccion,
        on_delete=models.CASCADE,
        related_name='detalle_lonas',
        verbose_name="Orden de Producción"
    )
    item = models.ForeignKey(
        OrdenProduccionItem,
        on_delete=models.SET_NULL,
        related_name='lonas_utilizadas',
        blank=True,
        null=True,
        verbose_name="Ítem (opcional)"
    )
    lona = models.ForeignKey(
        InventarioLona,
        on_delete=models.PROTECT,
        related_name='usos_en_ordenes',
        verbose_name="Rollo de Lona"
    )
    
    # Cantidades
    metros_requeridos = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Metros Requeridos"
    )
    metros_utilizados = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Metros Utilizados",
        help_text="Se llena al ejecutar el corte"
    )
    
    # Ejecución del Corte
    cortado_por = models.ForeignKey(
        'trabajadores.TrabajadorPersonal',
        on_delete=models.SET_NULL,
        related_name='cortes_lona_realizados',
        blank=True,
        null=True,
        verbose_name="Cortado Por"
    )
    fecha_corte = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de Corte"
    )
    observaciones_corte = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones del Corte"
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='PENDIENTE',
        verbose_name="Estado"
    )
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Registro"
    )

    class Meta:
        db_table = 'inv_orden_produccion_lona'
        verbose_name = 'Detalle Lona de Orden'
        verbose_name_plural = 'Detalle Lonas de Órdenes'
        ordering = ['orden', 'id']

    def __str__(self):
        return f"{self.orden} - {self.lona.codigo_rollo}: {self.metros_requeridos}m"


class OrdenProduccionEstructura(models.Model):
    """
    Detalle de estructura utilizada en una orden de producción.
    """
    
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('FABRICADO', 'Fabricado'),
        ('PINTADO', 'Pintado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    id = models.AutoField(primary_key=True)
    orden = models.ForeignKey(
        OrdenProduccion,
        on_delete=models.CASCADE,
        related_name='detalle_estructuras',
        verbose_name="Orden de Producción"
    )
    item = models.ForeignKey(
        OrdenProduccionItem,
        on_delete=models.SET_NULL,
        related_name='estructuras_utilizadas',
        blank=True,
        null=True,
        verbose_name="Ítem (opcional)"
    )
    estructura = models.ForeignKey(
        InventarioEstructura,
        on_delete=models.PROTECT,
        related_name='usos_en_ordenes',
        verbose_name="Lote de Estructura"
    )
    
    # Cantidades por Metros
    metros_requeridos = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Metros Requeridos"
    )
    metros_utilizados = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Metros Utilizados"
    )
    
    # Cantidades por Piezas
    piezas_requeridas = models.PositiveIntegerField(
        default=0,
        verbose_name="Piezas Requeridas"
    )
    piezas_utilizadas = models.PositiveIntegerField(
        default=0,
        verbose_name="Piezas Utilizadas"
    )
    
    # Ejecución
    fabricado_por = models.ForeignKey(
        'trabajadores.TrabajadorPersonal',
        on_delete=models.SET_NULL,
        related_name='estructuras_fabricadas',
        blank=True,
        null=True,
        verbose_name="Fabricado Por"
    )
    fecha_fabricacion = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de Fabricación"
    )
    pintado_por = models.ForeignKey(
        'trabajadores.TrabajadorPersonal',
        on_delete=models.SET_NULL,
        related_name='estructuras_pintadas',
        blank=True,
        null=True,
        verbose_name="Pintado Por"
    )
    fecha_pintado = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de Pintado"
    )
    
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='PENDIENTE',
        verbose_name="Estado"
    )
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Registro"
    )

    class Meta:
        db_table = 'inv_orden_produccion_estructura'
        verbose_name = 'Detalle Estructura de Orden'
        verbose_name_plural = 'Detalle Estructuras de Órdenes'
        ordering = ['orden', 'id']

    def __str__(self):
        return f"{self.orden} - {self.estructura.codigo_lote}"


class OrdenProduccionAccesorio(models.Model):
    """
    Detalle de accesorios utilizados en una orden de producción.
    """
    
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    id = models.AutoField(primary_key=True)
    orden = models.ForeignKey(
        OrdenProduccion,
        on_delete=models.CASCADE,
        related_name='detalle_accesorios',
        verbose_name="Orden de Producción"
    )
    item = models.ForeignKey(
        OrdenProduccionItem,
        on_delete=models.SET_NULL,
        related_name='accesorios_utilizados',
        blank=True,
        null=True,
        verbose_name="Ítem (opcional)"
    )
    accesorio = models.ForeignKey(
        InventarioAccesorio,
        on_delete=models.PROTECT,
        related_name='usos_en_ordenes',
        verbose_name="Accesorio"
    )
    
    # Cantidades
    cantidad_requerida = models.PositiveIntegerField(
        verbose_name="Cantidad Requerida"
    )
    cantidad_entregada = models.PositiveIntegerField(
        default=0,
        verbose_name="Cantidad Entregada"
    )
    
    # Ejecución
    entregado_por = models.ForeignKey(
        'trabajadores.TrabajadorPersonal',
        on_delete=models.SET_NULL,
        related_name='accesorios_entregados',
        blank=True,
        null=True,
        verbose_name="Entregado Por"
    )
    fecha_entrega = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de Entrega"
    )
    
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='PENDIENTE',
        verbose_name="Estado"
    )
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Registro"
    )

    class Meta:
        db_table = 'inv_orden_produccion_accesorio'
        verbose_name = 'Detalle Accesorio de Orden'
        verbose_name_plural = 'Detalle Accesorios de Órdenes'
        ordering = ['orden', 'id']

    def __str__(self):
        return f"{self.orden} - {self.accesorio.nombre}: {self.cantidad_requerida}"


# =============================================================================
# HISTORIAL DE MOVIMIENTOS (TRAZABILIDAD)
# =============================================================================

class HistorialInventario(models.Model):
    """
    Registro histórico de todos los movimientos de inventario.
    Proporciona trazabilidad completa de entradas, salidas y ajustes.
    """
    
    TIPO_MOVIMIENTO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('AJUSTE_POSITIVO', 'Ajuste Positivo'),
        ('AJUSTE_NEGATIVO', 'Ajuste Negativo'),
        ('RESERVA', 'Reserva'),
        ('LIBERACION', 'Liberación de Reserva'),
        ('DEVOLUCION', 'Devolución'),
        ('BAJA', 'Baja'),
    ]
    
    TIPO_INVENTARIO_CHOICES = [
        ('LONA', 'Lona'),
        ('ESTRUCTURA', 'Estructura'),
        ('ACCESORIO', 'Accesorio'),
    ]
    
    id_historial = models.AutoField(primary_key=True)
    fecha_movimiento = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha del Movimiento"
    )
    
    # Tipo de Movimiento
    tipo_movimiento = models.CharField(
        max_length=20,
        choices=TIPO_MOVIMIENTO_CHOICES,
        verbose_name="Tipo de Movimiento"
    )
    tipo_inventario = models.CharField(
        max_length=20,
        choices=TIPO_INVENTARIO_CHOICES,
        verbose_name="Tipo de Inventario"
    )
    
    # Referencias al Inventario (solo una será usada)
    lona = models.ForeignKey(
        InventarioLona,
        on_delete=models.SET_NULL,
        related_name='historial',
        blank=True,
        null=True,
        verbose_name="Lona"
    )
    estructura = models.ForeignKey(
        InventarioEstructura,
        on_delete=models.SET_NULL,
        related_name='historial',
        blank=True,
        null=True,
        verbose_name="Estructura"
    )
    accesorio = models.ForeignKey(
        InventarioAccesorio,
        on_delete=models.SET_NULL,
        related_name='historial',
        blank=True,
        null=True,
        verbose_name="Accesorio"
    )
    
    # Referencia a Orden de Producción
    orden_produccion = models.ForeignKey(
        OrdenProduccion,
        on_delete=models.SET_NULL,
        related_name='historial_movimientos',
        blank=True,
        null=True,
        verbose_name="Orden de Producción"
    )
    
    # Cantidades
    cantidad_anterior = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Cantidad Anterior"
    )
    cantidad_movimiento = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Cantidad del Movimiento"
    )
    cantidad_nueva = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Cantidad Nueva"
    )
    unidad_medida = models.CharField(
        max_length=20,
        verbose_name="Unidad de Medida",
        help_text="metros, unidades, piezas"
    )
    
    # Responsables
    ejecutado_por = models.ForeignKey(
        'trabajadores.TrabajadorPersonal',
        on_delete=models.SET_NULL,
        related_name='movimientos_ejecutados',
        blank=True,
        null=True,
        verbose_name="Ejecutado Por"
    )
    autorizado_por = models.ForeignKey(
        'trabajadores.TrabajadorPersonal',
        on_delete=models.SET_NULL,
        related_name='movimientos_autorizados',
        blank=True,
        null=True,
        verbose_name="Autorizado Por"
    )
    
    # Documentación
    documento_referencia = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Documento de Referencia",
        help_text="OP-1201, FAC-001, AJUSTE-001"
    )
    motivo = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Motivo"
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )
    
    # Auditoría
    registrado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='movimientos_registrados',
        blank=True,
        null=True,
        verbose_name="Registrado Por"
    )
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Registro"
    )

    class Meta:
        db_table = 'inv_historial_inventario'
        verbose_name = 'Historial de Inventario'
        verbose_name_plural = 'Historial de Inventario'
        ordering = ['-fecha_movimiento']

    def __str__(self):
        return f"{self.fecha_movimiento.strftime('%Y-%m-%d')} - {self.tipo_movimiento} - {self.tipo_inventario}"

    @property
    def item_inventario(self):
        """Retorna el ítem de inventario correspondiente"""
        if self.lona:
            return self.lona
        elif self.estructura:
            return self.estructura
        elif self.accesorio:
            return self.accesorio
        return None