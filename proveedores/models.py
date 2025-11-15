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

# NUEVO: Responsabilidades Fiscales
RESPONSABILIDAD_FISCAL_CHOICES = [
    ('NO_RESPONSABLE', 'No Responsable de IVA'),
    ('RESPONSABLE_IVA', 'Responsable de IVA'),
    ('GRAN_CONTRIBUYENTE', 'Gran Contribuyente'),
    ('AUTORRETENEDOR', 'Autorretenedor'),
    ('REGIMEN_SIMPLE', 'Régimen Simple de Tributación'),
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
    icono = models.CharField(max_length=50, blank=True, null=True, verbose_name="Icono")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    class Meta:
        db_table = 'tipos_proveedores'
        verbose_name = 'Tipo de Proveedor'
        verbose_name_plural = 'Tipos de Proveedores'
        ordering = ['nombre_tipo']
    
    def __str__(self):
        return self.nombre_tipo
    
    # ====== PROPIEDADES PARA VISUALIZACIÓN ======
    
    @property
    def icono_bootstrap(self):
        """
        Retorna el icono formateado para Bootstrap Icons
        Si el icono no tiene el prefijo 'bi-', lo añade
        """
        if self.icono:
            if not self.icono.startswith('bi-'):
                return f"bi-{self.icono}"
            return self.icono
        return "bi-building"  # Icono por defecto para tipos de proveedor
    
    @property
    def orden_visualizacion(self):
        """
        Retorna un orden de visualización basado en el ID
        """
        return self.id_tipo_proveedor


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
    
    # ====== NUEVAS PROPIEDADES AÑADIDAS ======
    
    @property
    def icono_bootstrap(self):
        """
        Retorna el icono formateado para Bootstrap Icons
        Si el icono no tiene el prefijo 'bi-', lo añade
        """
        if self.icono:
            if not self.icono.startswith('bi-'):
                return f"bi-{self.icono}"
            return self.icono
        return "bi-tag"  # Icono por defecto
    
    @property
    def color_badge(self):
        """
        Convierte el color hexadecimal a una clase de badge de Bootstrap
        Si no hay color definido, retorna 'secondary'
        """
        if not self.color:
            return 'secondary'
        
        # Mapeo de colores hex aproximados a clases Bootstrap
        color_mapping = {
            # Azules
            '#0d6efd': 'primary',
            '#0dcaf0': 'info',
            '#blue': 'primary',
            
            # Verdes
            '#198754': 'success',
            '#28a745': 'success',
            '#green': 'success',
            
            # Amarillos/Naranjas
            '#ffc107': 'warning',
            '#fd7e14': 'warning',
            '#yellow': 'warning',
            '#orange': 'warning',
            
            # Rojos
            '#dc3545': 'danger',
            '#red': 'danger',
            
            # Grises
            '#6c757d': 'secondary',
            '#gray': 'secondary',
            '#grey': 'secondary',
            
            # Oscuros
            '#212529': 'dark',
            '#black': 'dark',
            
            # Claros
            '#f8f9fa': 'light',
            '#white': 'light',
        }
        
        # Buscar coincidencia exacta (case insensitive)
        color_lower = self.color.lower()
        if color_lower in color_mapping:
            return color_mapping[color_lower]
        
        # Si es un color hex, intentar mapeo aproximado por luminosidad
        if self.color.startswith('#'):
            return self._get_badge_by_luminosity(self.color)
        
        # Por defecto
        return 'secondary'
    
    def _get_badge_by_luminosity(self, hex_color):
        """
        Calcula la luminosidad del color hex y retorna la clase Bootstrap más apropiada
        """
        try:
            # Remover el #
            hex_color = hex_color.lstrip('#')
            
            # Convertir a RGB
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])
            
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            # Calcular luminosidad (fórmula estándar)
            luminosity = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            
            # Decidir clase según dominancia de color y luminosidad
            if r > g and r > b:  # Dominante rojo
                return 'danger'
            elif g > r and g > b:  # Dominante verde
                return 'success'
            elif b > r and b > g:  # Dominante azul
                return 'primary' if luminosity < 0.5 else 'info'
            elif luminosity > 0.7:  # Muy claro
                return 'light'
            elif luminosity < 0.3:  # Muy oscuro
                return 'dark'
            else:  # Gris/neutral
                return 'secondary'
                
        except (ValueError, IndexError):
            return 'secondary'
    
    @property
    def color_hex_o_default(self):
        """
        Retorna el color hexadecimal o un color por defecto
        Útil para mostrar el color real en la UI
        """
        return self.color if self.color else '#6c757d'
    
    @property
    def orden_visualizacion(self):
        """
        Retorna un orden de visualización basado en el nombre
        Por ahora retorna el ID, pero puede personalizarse
        """
        return self.id_categoria

class TipoDocumentoProveedor(models.Model):
    """
    Catálogo de tipos de documentos que deben presentar los proveedores
    Ejemplos: RUT, Cámara de Comercio, Estados Financieros, etc.
    """
    id_tipo_documento = models.AutoField(primary_key=True)
    nombre_tipo_documento = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Tipo de Documento")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    icono = models.CharField(max_length=50, blank=True, null=True, verbose_name="Icono")
    obligatorio = models.BooleanField(default=False, verbose_name="Obligatorio")
    requiere_vigencia = models.BooleanField(default=True, verbose_name="Requiere Control de Vigencia")
    dias_alerta_vencimiento = models.IntegerField(
        default=30,
        blank=True,  # AÑADIDO: Permite campo vacío en formularios
        null=True,   # AÑADIDO: Permite NULL en base de datos
        verbose_name="Días de Alerta antes del Vencimiento",
        help_text="Días antes del vencimiento para enviar alertas (solo si requiere vigencia)"
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
    
    # NUEVO: Campo unificado para responsabilidades fiscales
    responsabilidad_fiscal = models.CharField(
        max_length=50,
        choices=RESPONSABILIDAD_FISCAL_CHOICES,
        default='RESPONSABLE_IVA',
        verbose_name="Responsabilidad Fiscal"
    )
    
    # Mantener campos antiguos por compatibilidad (deprecated)
    responsable_iva = models.BooleanField(default=True, verbose_name="Responsable de IVA")
    gran_contribuyente = models.BooleanField(default=False, verbose_name="Gran Contribuyente")
    autorretenedor = models.BooleanField(default=False, verbose_name="Autorretenedor")
    
    # NUEVO: Campos adicionales legales
    pais_origen = models.CharField(
        max_length=100,
        default='Colombia',
        verbose_name="País de Origen",
        help_text="País donde está constituida la empresa"
    )
    
    actividad_economica = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Actividad Económica",
        help_text="Descripción de la actividad económica principal"
    )
    
    codigo_ciiu = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Código CIIU",
        help_text="Clasificación Industrial Internacional Uniforme"
    )
    
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
    
    # NUEVO: Email específico para facturación
    email_facturacion = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email de Facturación",
        help_text="Email específico para envío de facturas"
    )
    
    sitio_web = models.URLField(blank=True, null=True, verbose_name="Sitio Web")
    
    # NUEVO: Horario de atención
    horario_atencion = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Horario de Atención",
        help_text="Ej: Lunes a Viernes 8:00 AM - 5:00 PM"
    )
    
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
    
    # NUEVO: Titular de la cuenta
    titular_cuenta = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Titular de la Cuenta",
        help_text="Nombre del titular de la cuenta bancaria"
    )
    
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
    
    # NUEVO: Acepta crédito
    acepta_credito = models.BooleanField(
        default=True,
        verbose_name="Acepta Crédito",
        help_text="¿El proveedor acepta ventas a crédito?"
    )
    
    # NUEVO: Métodos de pago
    metodos_pago_aceptados = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Métodos de Pago Aceptados",
        help_text="Ej: Efectivo, Transferencia, Cheque, Tarjeta"
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
    
    # ====== MÉTODOS PARA VISUALIZACIÓN ======
    
    def get_estado_badge_class(self):
        """
        Retorna la clase de badge de Bootstrap según el estado
        """
        if self.estado == 'ACTIVO':
            return 'bg-success'
        elif self.estado == 'INACTIVO':
            return 'bg-danger'
        else:
            return 'bg-secondary'
    
    def get_calificacion_estrellas(self):
        """
        Retorna la calificación en formato de estrellas (0-5)
        Retorna tupla: (estrellas_llenas, estrellas_medias, estrellas_vacias)
        """
        calificacion = float(self.calificacion) if self.calificacion else 0
        
        estrellas_llenas = int(calificacion)  # Parte entera
        tiene_media = (calificacion - estrellas_llenas) >= 0.5
        estrellas_medias = 1 if tiene_media else 0
        estrellas_vacias = 5 - estrellas_llenas - estrellas_medias
        
        return {
            'llenas': estrellas_llenas,
            'medias': estrellas_medias,
            'vacias': estrellas_vacias,
            'valor': calificacion
        }
    
    def get_calificacion_html(self):
        """
        Retorna HTML con estrellas para la calificación
        """
        estrellas = self.get_calificacion_estrellas()
        html = '<span class="text-warning">'
        
        # Estrellas llenas
        for i in range(estrellas['llenas']):
            html += '<i class="bi bi-star-fill"></i>'
        
        # Estrella media
        if estrellas['medias'] > 0:
            html += '<i class="bi bi-star-half"></i>'
        
        # Estrellas vacías
        for i in range(estrellas['vacias']):
            html += '<i class="bi bi-star"></i>'
        
        html += f'</span> <span class="text-muted small">({estrellas["valor"]:.1f}/5.0)</span>'
        return html
    
    @property
    def plazo_entrega_dias(self):
        """
        Compatibilidad: retorna tiempo_entrega_promedio
        """
        return self.tiempo_entrega_promedio
    
    @property
    def tiempo_credito_dias(self):
        """
        Extrae días de las condiciones de pago
        Si no puede extraer, retorna 0
        """
        if not self.condiciones_pago:
            return 0
        
        # Intentar extraer número de días
        import re
        match = re.search(r'(\d+)\s*d[ií]as?', self.condiciones_pago, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 0


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
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Área de Responsabilidad",
        help_text="Área o departamento del que es responsable"
    )
    
    telefono_fijo = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Teléfono Fijo"
    )
    
    telefono_movil = models.CharField(
        max_length=50,
        verbose_name="Teléfono Móvil"
    )
    
    email = models.EmailField(verbose_name="Email")
    
    es_contacto_principal = models.BooleanField(
        default=False,
        verbose_name="Contacto Principal",
        help_text="Solo puede haber un contacto principal por proveedor"
    )
    
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )
    
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Última Modificación")
    
    class Meta:
        db_table = 'contactos_proveedores'
        verbose_name = 'Contacto de Proveedor'
        verbose_name_plural = 'Contactos de Proveedores'
        ordering = ['-es_contacto_principal', 'apellidos', 'nombres']
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.id_proveedor.razon_social}"
    
    def get_nombre_completo(self):
        """Retorna el nombre completo del contacto"""
        return f"{self.nombres} {self.apellidos}"
    
    def save(self, *args, **kwargs):
        """
        Override save para asegurar que solo haya un contacto principal por proveedor
        """
        if self.es_contacto_principal:
            # Desactivar otros contactos principales del mismo proveedor
            ContactoProveedor.objects.filter(
                id_proveedor=self.id_proveedor,
                es_contacto_principal=True
            ).exclude(id_contacto=self.id_contacto).update(es_contacto_principal=False)
        
        super().save(*args, **kwargs)


# =====================================================
# MODELO DE DOCUMENTOS - FASE 4
# =====================================================

class DocumentoProveedor(models.Model):
    """
    Modelo para gestionar documentos digitales de proveedores
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
        related_name='documentos',
        verbose_name="Tipo de Documento"
    )
    
    archivo = models.FileField(
        upload_to='proveedores/documentos/%Y/%m/',
        verbose_name="Archivo",
        help_text="Archivo del documento (PDF, Word, Excel, Imagen)"
    )
    
    nombre_archivo_original = models.CharField(
        max_length=255,
        verbose_name="Nombre Original del Archivo"
    )
    
    numero_documento = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Número de Documento",
        help_text="Número de folio, certificado, etc."
    )
    
    fecha_emision = models.DateField(
        verbose_name="Fecha de Emisión"
    )
    
    fecha_vencimiento = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de Vencimiento",
        help_text="Dejar vacío si el documento no vence"
    )
    
    entidad_emisora = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Entidad Emisora",
        help_text="Organismo o entidad que emitió el documento"
    )
    
    estado_documento = models.CharField(
        max_length=20,
        choices=ESTADO_DOCUMENTO_CHOICES,
        default='VIGENTE',
        verbose_name="Estado del Documento"
    )
    
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )
    
    fecha_carga = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Carga"
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Modificación"
    )
    
    class Meta:
        db_table = 'documentos_proveedores'
        verbose_name = 'Documento de Proveedor'
        verbose_name_plural = 'Documentos de Proveedores'
        ordering = ['-fecha_carga']
    
    def __str__(self):
        return f"{self.id_tipo_documento.nombre_tipo_documento} - {self.id_proveedor.razon_social}"
    
    def actualizar_estado(self):
        """
        Actualiza el estado del documento según las fechas
        """
        from datetime import date, timedelta
        
        if not self.fecha_vencimiento:
            self.estado_documento = 'NO_APLICA'
            return
        
        hoy = date.today()
        dias_diferencia = (self.fecha_vencimiento - hoy).days
        dias_alerta = self.id_tipo_documento.dias_alerta_vencimiento
        
        if dias_diferencia < 0:
            self.estado_documento = 'VENCIDO'
        elif dias_diferencia <= dias_alerta:
            self.estado_documento = 'POR_VENCER'
        else:
            self.estado_documento = 'VIGENTE'
    
    def get_dias_para_vencer(self):
        """Retorna los días que faltan para el vencimiento"""
        from datetime import date
        
        if not self.fecha_vencimiento:
            return None
        
        hoy = date.today()
        return (self.fecha_vencimiento - hoy).days
    
    def get_badge_estado(self):
        """Retorna la clase CSS para el badge según el estado"""
        badges = {
            'VIGENTE': 'bg-success',
            'POR_VENCER': 'bg-warning',
            'VENCIDO': 'bg-danger',
            'NO_APLICA': 'bg-secondary'
        }
        return badges.get(self.estado_documento, 'bg-secondary')
    
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
    
    def get_tamano_archivo(self):
        """
        Retorna el tamaño del archivo formateado.
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
            for unit in ['bytes', 'KB', 'MB', 'GB']:
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