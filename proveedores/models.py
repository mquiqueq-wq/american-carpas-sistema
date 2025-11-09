"""
Modelos para el módulo de gestión de proveedores
American Carpas 1 SAS
Incluye: Catálogos, Proveedores, Contactos, Documentos y Productos/Servicios
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# =====================================================
# CHOICES GLOBALES
# =====================================================

ESTADO_CHOICES = [
    ('ACTIVO', 'Activo'),
    ('INACTIVO', 'Inactivo'),
]

TIPO_DOCUMENTO_CHOICES = [
    ('NIT', 'NIT'),
    ('CC', 'Cédula de Ciudadanía'),
    ('CE', 'Cédula de Extranjería'),
    ('PASAPORTE', 'Pasaporte'),
]

TIPO_PERSONA_CHOICES = [
    ('JURIDICA', 'Persona Jurídica'),
    ('NATURAL', 'Persona Natural'),
]

AREA_RESPONSABILIDAD_CHOICES = [
    ('COMERCIAL', 'Comercial'),
    ('TECNICA', 'Técnica'),
    ('FINANCIERA', 'Financiera'),
    ('LOGISTICA', 'Logística'),
    ('CALIDAD', 'Calidad'),
    ('ADMINISTRATIVA', 'Administrativa'),
    ('OTRA', 'Otra'),
]

ESTADO_DOCUMENTO_CHOICES = [
    ('VIGENTE', 'Vigente'),
    ('POR_VENCER', 'Por vencer'),
    ('VENCIDO', 'Vencido'),
    ('NO_APLICA', 'No aplica'),
]

TIPO_PRODUCTO_SERVICIO_CHOICES = [
    ('PRODUCTO', 'Producto'),
    ('SERVICIO', 'Servicio'),
    ('AMBOS', 'Producto y Servicio'),
]

UNIDAD_MEDIDA_CHOICES = [
    ('UNIDAD', 'Unidad'),
    ('METRO', 'Metro'),
    ('METRO_CUADRADO', 'Metro cuadrado'),
    ('KILOGRAMO', 'Kilogramo'),
    ('LITRO', 'Litro'),
    ('CAJA', 'Caja'),
    ('PAQUETE', 'Paquete'),
    ('ROLLO', 'Rollo'),
    ('SERVICIO', 'Servicio'),
    ('OTRO', 'Otro'),
]

MONEDA_CHOICES = [
    ('COP', 'Pesos colombianos (COP)'),
    ('USD', 'Dólares (USD)'),
    ('EUR', 'Euros (EUR)'),
]


# =====================================================
# MODELOS DE CATÁLOGOS - FASE 1
# =====================================================

class TipoProveedor(models.Model):
    """
    Catálogo de tipos de proveedores
    Ejemplos: Fabricante, Distribuidor, Importador, etc.
    """
    id_tipo_proveedor = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Tipo")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    class Meta:
        db_table = 'tipos_proveedores'
        verbose_name = 'Tipo de Proveedor'
        verbose_name_plural = 'Tipos de Proveedores'
        ordering = ['nombre_tipo']
    
    def __str__(self):
        return self.nombre_tipo


class CategoriaProveedor(models.Model):
    """
    Catálogo de categorías de proveedores con jerarquía
    Ejemplos: Textiles, Metalmecánica, Servicios, etc.
    """
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    categoria_padre = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategorias',
        verbose_name="Categoría Padre"
    )
    icono = models.CharField(max_length=50, blank=True, null=True, verbose_name="Icono")
    color = models.CharField(max_length=20, blank=True, null=True, verbose_name="Color")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    class Meta:
        db_table = 'categorias_proveedores'
        verbose_name = 'Categoría de Proveedor'
        verbose_name_plural = 'Categorías de Proveedores'
        ordering = ['nombre_categoria']
    
    def __str__(self):
        if self.categoria_padre:
            return f"{self.categoria_padre.nombre_categoria} > {self.nombre_categoria}"
        return self.nombre_categoria
    
    def get_nivel(self):
        """Retorna el nivel de jerarquía de la categoría"""
        nivel = 0
        categoria_actual = self
        while categoria_actual.categoria_padre:
            nivel += 1
            categoria_actual = categoria_actual.categoria_padre
        return nivel


class TipoDocumentoProveedor(models.Model):
    """
    Catálogo de tipos de documentos que deben presentar los proveedores
    Ejemplos: RUT, Cámara de Comercio, Estados Financieros, etc.
    """
    id_tipo_documento = models.AutoField(primary_key=True)
    nombre_tipo_documento = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Tipo de Documento")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    obligatorio = models.BooleanField(default=False, verbose_name="Obligatorio")
    requiere_vigencia = models.BooleanField(default=True, verbose_name="Requiere Control de Vigencia")
    dias_alerta_vencimiento = models.IntegerField(
        default=30,
        verbose_name="Días de Alerta antes del Vencimiento",
        help_text="Días antes del vencimiento para enviar alertas"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    class Meta:
        db_table = 'tipos_documentos_proveedores'
        verbose_name = 'Tipo de Documento de Proveedor'
        verbose_name_plural = 'Tipos de Documentos de Proveedores'
        ordering = ['nombre_tipo_documento']
    
    def __str__(self):
        return self.nombre_tipo_documento


# =====================================================
# MODELO PRINCIPAL: PROVEEDOR - FASE 2
# =====================================================

class Proveedor(models.Model):
    """
    Modelo principal para gestión de proveedores
    Contiene toda la información del proveedor
    """
    id_proveedor = models.AutoField(primary_key=True)
    
    # ===== IDENTIFICACIÓN BÁSICA =====
    tipo_persona = models.CharField(
        max_length=20,
        choices=TIPO_PERSONA_CHOICES,
        default='JURIDICA',
        verbose_name="Tipo de Persona"
    )
    
    razon_social = models.CharField(
        max_length=200,
        verbose_name="Razón Social",
        help_text="Nombre legal completo del proveedor"
    )
    
    nombre_comercial = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Nombre Comercial",
        help_text="Nombre con el que opera comercialmente"
    )
    
    tipo_documento = models.CharField(
        max_length=20,
        choices=TIPO_DOCUMENTO_CHOICES,
        default='NIT',
        verbose_name="Tipo de Documento"
    )
    
    numero_documento = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Número de Documento",
        help_text="NIT, CC, CE o Pasaporte"
    )
    
    digito_verificacion = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Dígito de Verificación",
        help_text="Solo para NIT"
    )
    
    # ===== CLASIFICACIÓN =====
    tipo_proveedor = models.ForeignKey(
        TipoProveedor,
        on_delete=models.PROTECT,
        related_name='proveedores',
        verbose_name="Tipo de Proveedor"
    )
    
    categoria_principal = models.ForeignKey(
        CategoriaProveedor,
        on_delete=models.PROTECT,
        related_name='proveedores',
        verbose_name="Categoría Principal"
    )
    
    # ===== INFORMACIÓN LEGAL Y TRIBUTARIA =====
    regimen_tributario = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Régimen Tributario",
        help_text="Ej: Régimen Común, Régimen Simplificado"
    )
    
    responsable_iva = models.BooleanField(default=True, verbose_name="Responsable de IVA")
    gran_contribuyente = models.BooleanField(default=False, verbose_name="Gran Contribuyente")
    autorretenedor = models.BooleanField(default=False, verbose_name="Autorretenedor")
    
    # ===== INFORMACIÓN DE CONTACTO =====
    pais = models.CharField(max_length=100, default='Colombia', verbose_name="País")
    departamento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Departamento/Estado")
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    codigo_postal = models.CharField(max_length=20, blank=True, null=True, verbose_name="Código Postal")
    
    telefono_principal = models.CharField(max_length=50, verbose_name="Teléfono Principal")
    telefono_secundario = models.CharField(max_length=50, blank=True, null=True, verbose_name="Teléfono Secundario")
    email_principal = models.EmailField(verbose_name="Email Principal")
    email_secundario = models.EmailField(blank=True, null=True, verbose_name="Email Secundario")
    sitio_web = models.URLField(blank=True, null=True, verbose_name="Sitio Web")
    
    # ===== INFORMACIÓN BANCARIA =====
    banco = models.CharField(max_length=100, blank=True, null=True, verbose_name="Banco")
    tipo_cuenta = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Tipo de Cuenta",
        help_text="Ahorros, Corriente"
    )
    numero_cuenta = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número de Cuenta")
    
    # ===== INFORMACIÓN COMERCIAL =====
    tiempo_entrega_promedio = models.IntegerField(
        default=0,
        verbose_name="Tiempo de Entrega Promedio (días)"
    )
    
    condiciones_pago = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Condiciones de Pago",
        help_text="Ej: 30 días, Contado, etc."
    )
    
    monto_minimo_pedido = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Monto Mínimo de Pedido"
    )
    
    descuento_pronto_pago = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Descuento por Pronto Pago (%)"
    )
    
    calificacion = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        verbose_name="Calificación",
        help_text="De 0.00 a 5.00",
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    
    # ===== OBSERVACIONES Y NOTAS =====
    notas_internas = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notas Internas",
        help_text="Información privada, no visible para el proveedor"
    )
    
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones Generales")
    
    # ===== CONTROL =====
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='ACTIVO',
        verbose_name="Estado"
    )
    
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Última Modificación")
    
    class Meta:
        db_table = 'proveedores'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['razon_social']
    
    def __str__(self):
        return self.razon_social
    
    def get_documento_completo(self):
        """Retorna el número de documento con dígito de verificación si aplica"""
        if self.digito_verificacion:
            return f"{self.numero_documento}-{self.digito_verificacion}"
        return self.numero_documento
    
    def get_direccion_completa(self):
        """Retorna la dirección completa formateada"""
        partes = [self.direccion, self.ciudad]
        if self.departamento:
            partes.append(self.departamento)
        partes.append(self.pais)
        return ", ".join(partes)


# =====================================================
# MODELO DE CONTACTOS - FASE 3
# =====================================================

class ContactoProveedor(models.Model):
    """
    Modelo para gestionar múltiples contactos de cada proveedor
    """
    id_contacto = models.AutoField(primary_key=True)
    
    id_proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name='contactos',
        verbose_name="Proveedor"
    )
    
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    cargo = models.CharField(max_length=100, verbose_name="Cargo")
    
    area_responsabilidad = models.CharField(
        max_length=50,
        choices=AREA_RESPONSABILIDAD_CHOICES,
        default='COMERCIAL',
        verbose_name="Área de Responsabilidad"
    )
    
    telefono_fijo = models.CharField(max_length=50, blank=True, null=True, verbose_name="Teléfono Fijo")
    telefono_movil = models.CharField(max_length=50, verbose_name="Teléfono Móvil")
    email = models.EmailField(verbose_name="Email")
    
    es_contacto_principal = models.BooleanField(default=False, verbose_name="Contacto Principal")
    
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Última Modificación")
    
    class Meta:
        db_table = 'contactos_proveedores'
        verbose_name = 'Contacto de Proveedor'
        verbose_name_plural = 'Contactos de Proveedores'
        ordering = ['-es_contacto_principal', 'nombres']
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.cargo})"
    
    def get_nombre_completo(self):
        """Retorna el nombre completo del contacto"""
        return f"{self.nombres} {self.apellidos}"
    
    def save(self, *args, **kwargs):
        """
        Si este contacto es marcado como principal, 
        desmarcar cualquier otro contacto principal del mismo proveedor
        """
        if self.es_contacto_principal:
            ContactoProveedor.objects.filter(
                id_proveedor=self.id_proveedor,
                es_contacto_principal=True
            ).update(es_contacto_principal=False)
        super().save(*args, **kwargs)


# =====================================================
# MODELO DE DOCUMENTOS - FASE 4
# =====================================================

class DocumentoProveedor(models.Model):
    """
    Modelo para gestionar documentos de proveedores
    Con control de vigencia y alertas de vencimiento
    """
    id_documento = models.AutoField(primary_key=True)
    
    id_proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name='documentos',
        verbose_name="Proveedor"
    )
    
    id_tipo_documento = models.ForeignKey(
        TipoDocumentoProveedor,
        on_delete=models.PROTECT,
        related_name='documentos_proveedores',
        verbose_name="Tipo de Documento"
    )
    
    archivo = models.FileField(
        upload_to='documentos_proveedores/%Y/%m/',
        verbose_name="Archivo",
        help_text="Archivo PDF, imagen o documento escaneado"
    )
    
    nombre_archivo_original = models.CharField(
        max_length=255,
        verbose_name="Nombre del Archivo",
        help_text="Nombre original del archivo subido"
    )
    
    numero_documento = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Número de Documento",
        help_text="Número de folio, certificado, etc."
    )
    
    fecha_emision = models.DateField(verbose_name="Fecha de Emisión")
    
    fecha_vencimiento = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de Vencimiento",
        help_text="Dejar vacío si el documento no vence"
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_DOCUMENTO_CHOICES,
        default='VIGENTE',
        verbose_name="Estado"
    )
    
    entidad_emisora = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Entidad Emisora",
        help_text="Ej: Cámara de Comercio, DIAN, etc."
    )
    
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    
    fecha_carga = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Carga")
    
    cargado_por = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Cargado Por",
        help_text="Usuario que cargó el documento"
    )
    
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Última Modificación")
    
    class Meta:
        db_table = 'documentos_proveedores'
        verbose_name = 'Documento de Proveedor'
        verbose_name_plural = 'Documentos de Proveedores'
        ordering = ['-fecha_carga']
        unique_together = [['id_proveedor', 'id_tipo_documento']]
    
    def __str__(self):
        return f"{self.id_tipo_documento.nombre_tipo_documento} - {self.id_proveedor.razon_social}"
    
    def save(self, *args, **kwargs):
        """Guardar nombre del archivo y actualizar estado automáticamente"""
        if self.archivo and not self.nombre_archivo_original:
            self.nombre_archivo_original = self.archivo.name
        
        self.actualizar_estado()
        
        super().save(*args, **kwargs)
    
    def actualizar_estado(self):
        """Actualizar el estado del documento según su vigencia"""
        from datetime import date
        
        if not self.fecha_vencimiento:
            self.estado = 'NO_APLICA'
            return
        
        hoy = date.today()
        dias_diferencia = (self.fecha_vencimiento - hoy).days
        
        dias_alerta = self.id_tipo_documento.dias_alerta_vencimiento
        
        if self.fecha_vencimiento < hoy:
            self.estado = 'VENCIDO'
        elif dias_diferencia <= dias_alerta:
            self.estado = 'POR_VENCER'
        else:
            self.estado = 'VIGENTE'
    
    def get_estado_badge_class(self):
        """Retorna la clase CSS para el badge de estado"""
        estados = {
            'VIGENTE': 'bg-success',
            'POR_VENCER': 'bg-warning',
            'VENCIDO': 'bg-danger',
            'NO_APLICA': 'bg-secondary'
        }
        return estados.get(self.estado, 'bg-secondary')
    
    def dias_para_vencimiento(self):
        """Retorna los días que faltan para el vencimiento"""
        from datetime import date
        
        if not self.fecha_vencimiento:
            return None
        
        hoy = date.today()
        return (self.fecha_vencimiento - hoy).days
    
    def esta_vigente(self):
        """Verifica si el documento está vigente"""
        return self.estado in ['VIGENTE', 'NO_APLICA']
    
    def get_tamano_archivo(self):
        """Retorna el tamaño del archivo en formato legible"""
        try:
            size = self.archivo.size
            if size < 1024:
                return f"{size} bytes"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            else:
                return f"{size / (1024 * 1024):.1f} MB"
        except:
            return "N/A"
    
    def get_extension_archivo(self):
        """Retorna la extensión del archivo"""
        import os
        return os.path.splitext(self.nombre_archivo_original)[1].lower()
    
    def get_icono_archivo(self):
        """Retorna el icono apropiado según el tipo de archivo"""
        extension = self.get_extension_archivo()
        iconos = {
            '.pdf': 'bi-file-pdf',
            '.doc': 'bi-file-word',
            '.docx': 'bi-file-word',
            '.xls': 'bi-file-excel',
            '.xlsx': 'bi-file-excel',
            '.jpg': 'bi-file-image',
            '.jpeg': 'bi-file-image',
            '.png': 'bi-file-image',
            '.zip': 'bi-file-zip',
            '.rar': 'bi-file-zip',
        }
        return iconos.get(extension, 'bi-file-earmark')


# =====================================================
# MODELO DE PRODUCTOS/SERVICIOS - FASE 5
# =====================================================

class ProductoServicioProveedor(models.Model):
    """
    Modelo para gestionar el catálogo de productos/servicios de cada proveedor
    """
    id_producto_servicio = models.AutoField(primary_key=True)
    
    id_proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name='productos_servicios',
        verbose_name="Proveedor"
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_PRODUCTO_SERVICIO_CHOICES,
        default='PRODUCTO',
        verbose_name="Tipo"
    )
    
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre del Producto/Servicio"
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción",
        help_text="Descripción detallada del producto o servicio"
    )
    
    sku_codigo = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="SKU / Código",
        help_text="Código o referencia del proveedor"
    )
    
    marca = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Marca",
        help_text="Marca del producto (si aplica)"
    )
    
    unidad_medida = models.CharField(
        max_length=30,
        choices=UNIDAD_MEDIDA_CHOICES,
        default='UNIDAD',
        verbose_name="Unidad de Medida"
    )
    
    # Precios
    precio_unitario = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Precio Unitario",
        validators=[MinValueValidator(0)]
    )
    
    moneda = models.CharField(
        max_length=3,
        choices=MONEDA_CHOICES,
        default='COP',
        verbose_name="Moneda"
    )
    
    precio_especial = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Precio Especial",
        help_text="Precio con descuento o promocional (opcional)",
        validators=[MinValueValidator(0)]
    )
    
    descuento_porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Descuento (%)",
        help_text="Descuento aplicable",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Condiciones comerciales
    cantidad_minima = models.IntegerField(
        default=1,
        verbose_name="Cantidad Mínima de Compra",
        validators=[MinValueValidator(1)]
    )
    
    tiempo_entrega_dias = models.IntegerField(
        default=0,
        verbose_name="Tiempo de Entrega (días)",
        validators=[MinValueValidator(0)]
    )
    
    disponible = models.BooleanField(
        default=True,
        verbose_name="Disponible",
        help_text="Si está disponible para compra actualmente"
    )
    
    stock_disponible = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Stock Disponible",
        help_text="Cantidad en stock (opcional)",
        validators=[MinValueValidator(0)]
    )
    
    # Información adicional
    especificaciones_tecnicas = models.TextField(
        blank=True,
        null=True,
        verbose_name="Especificaciones Técnicas",
        help_text="Detalles técnicos, dimensiones, materiales, etc."
    )
    
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Modificación"
    )
    
    fecha_ultima_actualizacion_precio = models.DateField(
        blank=True,
        null=True,
        verbose_name="Última Actualización de Precio"
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Si el producto está activo en el catálogo"
    )
    
    class Meta:
        db_table = 'productos_servicios_proveedores'
        verbose_name = 'Producto/Servicio de Proveedor'
        verbose_name_plural = 'Productos/Servicios de Proveedores'
        ordering = ['nombre']
        unique_together = [['id_proveedor', 'sku_codigo']]
    
    def __str__(self):
        return f"{self.nombre} - {self.id_proveedor.razon_social}"
    
    def get_precio_final(self):
        """Retorna el precio final considerando descuentos"""
        if self.precio_especial:
            return self.precio_especial
        
        if self.descuento_porcentaje > 0:
            descuento = self.precio_unitario * (self.descuento_porcentaje / 100)
            return self.precio_unitario - descuento
        
        return self.precio_unitario
    
    def get_ahorro(self):
        """Retorna el ahorro si hay precio especial o descuento"""
        precio_final = self.get_precio_final()
        if precio_final < self.precio_unitario:
            return self.precio_unitario - precio_final
        return 0
    
    def get_precio_formateado(self):
        """Retorna el precio formateado con símbolo de moneda"""
        simbolos = {
            'COP': '$',
            'USD': 'US$',
            'EUR': '€'
        }
        simbolo = simbolos.get(self.moneda, '$')
        precio = self.get_precio_final()
        return f"{simbolo} {precio:,.2f}"
    
    def tiene_descuento(self):
        """Verifica si tiene algún tipo de descuento"""
        return self.precio_especial or self.descuento_porcentaje > 0
    
    def get_badge_disponibilidad(self):
        """Retorna la clase CSS para el badge de disponibilidad"""
        if not self.activo:
            return 'bg-secondary'
        elif not self.disponible:
            return 'bg-warning'
        elif self.stock_disponible is not None and self.stock_disponible == 0:
            return 'bg-danger'
        else:
            return 'bg-success'
    
    def get_texto_disponibilidad(self):
        """Retorna el texto de disponibilidad"""
        if not self.activo:
            return 'Inactivo'
        elif not self.disponible:
            return 'No disponible'
        elif self.stock_disponible is not None and self.stock_disponible == 0:
            return 'Sin stock'
        else:
            return 'Disponible'