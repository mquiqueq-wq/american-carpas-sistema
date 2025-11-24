# Módulo de Inventarios - American Carpas 1 SAS

## 📋 Descripción

Este módulo proporciona una gestión completa de inventarios para empresas de ingeniería civil y fabricación de carpas. Incluye:

- **Inventario General**: Equipos mayores, maquinaria pesada, herramientas, EPP, consumibles, mobiliario
- **Inventario de Carpas**: Lonas (por rollo), estructuras (por lote), accesorios
- **Sistema de Movimientos**: Entradas, salidas, transferencias, ajustes, devoluciones
- **Asignaciones**: A proyectos y/o trabajadores con trazabilidad completa
- **Mantenimientos**: Programación y registro de mantenimientos preventivos/correctivos
- **Control de Combustible**: Para maquinaria pesada
- **Sistema de Alertas**: Stock mínimo, vencimientos, mantenimientos pendientes
- **Códigos QR**: Para identificación y escaneo de artículos

---

## 🚀 Instalación

### Paso 1: Copiar la carpeta del módulo

Copia la carpeta `inventario` completa a la raíz de tu proyecto Django (al mismo nivel que `trabajadores`, `proveedores`, `proyectos`).

```
american_carpas/
├── american_carpas_project/
├── trabajadores/
├── proveedores/
├── proyectos/
├── inventario/          <-- Nueva carpeta
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   └── fixtures/
│       └── datos_iniciales.json
├── templates/
├── static/
└── manage.py
```

### Paso 2: Registrar la aplicación

Agrega `'inventario'` a `INSTALLED_APPS` en `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'trabajadores',
    'proveedores',
    'proyectos',
    'inventario',  # <-- Agregar esta línea
]
```

### Paso 3: Crear y aplicar migraciones

```bash
# Crear las migraciones
python manage.py makemigrations inventario

# Aplicar las migraciones
python manage.py migrate
```

### Paso 4: Cargar datos iniciales

```bash
python manage.py loaddata inventario/fixtures/datos_iniciales.json
```

Este comando cargará:
- 7 Tipos de movimiento (Entrada, Salida, Transferencia, etc.)
- 4 Tipos de ubicación (Bodega, Proyecto, Vehículo, Taller)
- 9 Unidades de medida
- 6 Estados de artículo
- 6 Categorías de inventario
- 19 Subcategorías
- 4 Tipos de mantenimiento
- 5 Tipos de alerta
- 3 Calidades de material

### Paso 5: Verificar en el Admin

Accede a `http://localhost:8000/admin/` y verifica que aparezcan todas las secciones del módulo de inventarios.

---

## 📊 Estructura de Modelos

### Fase 1: Catálogos Base
| Modelo | Descripción |
|--------|-------------|
| `TipoUbicacion` | Tipos de ubicación (Bodega, Proyecto, etc.) |
| `Ubicacion` | Ubicaciones físicas del inventario |
| `UnidadMedida` | Unidades de medida (m, ud, kg, etc.) |
| `EstadoArticulo` | Estados posibles (Disponible, En uso, etc.) |
| `MarcaEquipo` | Marcas de equipos y maquinaria |

### Fase 2: Categorías
| Modelo | Descripción |
|--------|-------------|
| `CategoriaInventario` | Categorías principales con configuración de comportamiento |
| `SubcategoriaInventario` | Subcategorías vinculadas a categorías |

### Fase 3: Inventario General
| Modelo | Descripción |
|--------|-------------|
| `ArticuloInventario` | Modelo principal para todos los artículos |

### Fase 4: Inventario de Carpas
| Modelo | Descripción |
|--------|-------------|
| `TipoLona`, `AnchoLona`, `ColorLona` | Catálogos de lonas |
| `TipoEstructura`, `MedidaTubo`, `Calibre` | Catálogos de estructuras |
| `TipoAccesorioCarpa`, `CalidadMaterial` | Catálogos adicionales |
| `LoteLona` | Lotes/rollos de lona |
| `LoteEstructura` | Lotes de estructura |
| `AccesorioCarpa` | Accesorios de carpas |

### Fase 5: Movimientos
| Modelo | Descripción |
|--------|-------------|
| `TipoMovimiento` | Tipos de movimiento con configuración |
| `MovimientoInventario` | Registro de todos los movimientos (Kardex) |

### Fase 6: Asignaciones y Mantenimientos
| Modelo | Descripción |
|--------|-------------|
| `AsignacionInventario` | Asignaciones a proyectos/trabajadores |
| `TipoMantenimiento` | Tipos de mantenimiento |
| `MantenimientoEquipo` | Registro de mantenimientos |
| `RegistroCombustible` | Control de combustible |

### Fase 7: Alertas
| Modelo | Descripción |
|--------|-------------|
| `TipoAlerta` | Tipos de alerta del sistema |
| `AlertaInventario` | Alertas generadas |

---

## 🔗 Integraciones con otros módulos

El módulo de inventarios se integra con:

### Módulo de Proyectos (`proyectos`)
```python
from proyectos.models import Proyecto

# En AsignacionInventario, MovimientoInventario
proyecto = models.ForeignKey('proyectos.Proyecto', ...)

# En Ubicacion (para ubicaciones tipo proyecto)
proyecto = models.ForeignKey('proyectos.Proyecto', ...)
```

### Módulo de Trabajadores (`trabajadores`)
```python
from trabajadores.models import TrabajadorPersonal

# En AsignacionInventario, MovimientoInventario, RegistroCombustible
trabajador_responsable = models.ForeignKey('trabajadores.TrabajadorPersonal', ...)
```

### Módulo de Proveedores (`proveedores`)
```python
from proveedores.models import Proveedor

# En ArticuloInventario, LoteLona, LoteEstructura, etc.
proveedor = models.ForeignKey('proveedores.Proveedor', ...)
```

---

## 📝 Uso Básico

### Crear una ubicación
```python
from inventario.models import TipoUbicacion, Ubicacion

tipo_bodega = TipoUbicacion.objects.get(nombre='Bodega')
ubicacion = Ubicacion.objects.create(
    tipo_ubicacion=tipo_bodega,
    codigo='BOD-001',
    nombre='Bodega Principal',
    direccion='Calle 123 # 45-67',
    ciudad='Bogotá',
    responsable='Juan Pérez'
)
```

### Crear un artículo de inventario
```python
from inventario.models import ArticuloInventario, SubcategoriaInventario, UnidadMedida, EstadoArticulo, Ubicacion

subcategoria = SubcategoriaInventario.objects.get(codigo='EQM-COMP')
unidad = UnidadMedida.objects.get(abreviatura='ud')
estado = EstadoArticulo.objects.get(nombre='Disponible')
ubicacion = Ubicacion.objects.get(codigo='BOD-001')

articulo = ArticuloInventario.objects.create(
    nombre='Apisonador Tipo Canguro',
    subcategoria=subcategoria,
    unidad_medida=unidad,
    estado=estado,
    ubicacion_actual=ubicacion,
    cantidad_total=1,
    cantidad_disponible=1
)
# El código interno se genera automáticamente: EQM-0001
```

### Registrar un movimiento
```python
from inventario.models import MovimientoInventario, TipoMovimiento
from django.utils import timezone

tipo_entrada = TipoMovimiento.objects.get(codigo='ENT')

movimiento = MovimientoInventario.objects.create(
    tipo_movimiento=tipo_entrada,
    fecha_movimiento=timezone.now(),
    tipo_inventario='GENERAL',
    articulo_general=articulo,
    cantidad=1,
    unidad_medida='ud',
    cantidad_anterior=0,
    cantidad_nueva=1,
    ubicacion_origen=ubicacion,
    registrado_por=request.user
)
# El número de documento se genera automáticamente: MOV-2024-00001
```

### Crear un lote de lona
```python
from inventario.models import LoteLona, TipoLona, AnchoLona, ColorLona

tipo = TipoLona.objects.get(nombre='Lona PVC')
ancho = AnchoLona.objects.get(valor_metros=2.5)
color = ColorLona.objects.get(nombre='Blanco')

lote = LoteLona.objects.create(
    tipo_lona=tipo,
    ancho_lona=ancho,
    color_lona=color,
    metros_iniciales=100,
    metros_disponibles=100,
    costo_por_metro=25000,
    ubicacion=ubicacion,
    fecha_ingreso='2024-01-15'
)
# El código se genera automáticamente: LON-0001
```

---

## 🔧 Configuración de Categorías

Las categorías tienen configuraciones especiales que determinan el comportamiento de los artículos:

| Campo | Descripción |
|-------|-------------|
| `maneja_individual` | Cada artículo tiene número de serie único |
| `requiere_mantenimiento` | Los artículos requieren mantenimiento programado |
| `control_vencimiento` | Para EPP con fecha de vencimiento |
| `control_horometro` | Para maquinaria con horómetro |
| `control_combustible` | Para maquinaria y vehículos |

### Categorías predefinidas:

| Categoría | Individual | Mantenim. | Vencim. | Horómetro | Combustible |
|-----------|:----------:|:---------:|:-------:|:---------:|:-----------:|
| Equipos Mayores | ✓ | ✓ | - | - | - |
| Maquinaria Pesada | ✓ | ✓ | - | ✓ | ✓ |
| Herramienta Menor | - | - | - | - | - |
| Equipos de Seguridad | ✓ | ✓ | ✓ | - | - |
| Consumibles | - | - | - | - | - |
| Mobiliario/Oficina | ✓ | - | - | - | - |

---

## 📱 Códigos QR

Cada artículo, lote y accesorio tiene un `codigo_qr` único (UUID) que se genera automáticamente al crear el registro.

Para implementar la funcionalidad de escaneo QR, puedes usar la librería `qrcode`:

```bash
pip install qrcode[pil]
```

```python
import qrcode
from inventario.models import ArticuloInventario

articulo = ArticuloInventario.objects.get(pk=1)
url = f"https://tuapp.com/inventario/qr/{articulo.codigo_qr}/"

qr = qrcode.make(url)
qr.save(f"qr_{articulo.codigo_interno}.png")
```

---

## 🚀 Próximos Pasos

Después de instalar el módulo, las siguientes fases de desarrollo serán:

1. **Vistas y Templates**: Crear las vistas para CRUD de artículos, movimientos, asignaciones
2. **Dashboard**: Panel con estadísticas, alertas y gráficos
3. **Reportes**: Kardex, valorizado, movimientos por período
4. **API**: Endpoints para app móvil y escaneo QR
5. **Permisos**: Configuración de roles y permisos por usuario

---

## 📄 Licencia

Desarrollado como proyecto de tesis para American Carpas 1 SAS
Universidad La Gran Colombia

Autor: Mario
Versión: 1.0
Fecha: 2024
