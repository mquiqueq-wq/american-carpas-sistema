"""
Datos de prueba para el sistema de gestión de trabajadores - American Carpas
Generado para llenar las tablas del modelo Django
"""

from datetime import date, timedelta

# ============================================================================
# 1. DATOS DE 10 TRABAJADORES (TrabajadorPersonal)
# ============================================================================

trabajadores_data = [
    {
        'id_trabajador': '1098765432',
        'tipo_documento': 'CC',
        'nombres': 'Carlos Andrés',
        'apellidos': 'Rodríguez Gómez',
        'fecha_expedicion_doc': date(2015, 3, 15),
        'lugar_expedicion': 'Medellín',
        'nacionalidad': 'Colombiana',
        'fecha_nacimiento': date(1992, 5, 20),
        'lugar_nacimiento': 'Medellín',
        'genero': 'M',
        'estado_civil': 'CASADO',
        'direccion_residencia': 'Calle 45 #23-15',
        'ciudad_residencia': 'Medellín',
        'departamento_residencia': 'Antioquia',
        'telefono_celular': '3201234567',
        'correo_personal': 'carlos.rodriguez@email.com',
        'grupo_sanguineo_rh': 'O+',
        'nombres_padre': 'José Rodríguez',
        'nombres_madre': 'María Gómez',
        'nombre_contacto_emergencia': 'Ana Rodríguez (Esposa)',
        'numero_contacto_emergencia': '3109876543',
        'numero_hijos': 2,
        'cuenta_bancaria': '123456789',
        'tipo_cuenta': 'AHORROS',
        'banco': 'Bancolombia'
    },
    {
        'id_trabajador': '1023456789',
        'tipo_documento': 'CC',
        'nombres': 'María Fernanda',
        'apellidos': 'López Martínez',
        'fecha_expedicion_doc': date(2016, 8, 22),
        'lugar_expedicion': 'Bello',
        'nacionalidad': 'Colombiana',
        'fecha_nacimiento': date(1995, 11, 8),
        'lugar_nacimiento': 'Bello',
        'genero': 'F',
        'estado_civil': 'SOLTERA',
        'direccion_residencia': 'Carrera 80 #50-30 Apto 402',
        'ciudad_residencia': 'Medellín',
        'departamento_residencia': 'Antioquia',
        'telefono_celular': '3154567890',
        'correo_personal': 'maria.lopez@email.com',
        'grupo_sanguineo_rh': 'A+',
        'nombres_padre': 'Fernando López',
        'nombres_madre': 'Sandra Martínez',
        'nombre_contacto_emergencia': 'Sandra Martínez (Madre)',
        'numero_contacto_emergencia': '3002345678',
        'numero_hijos': 0,
        'cuenta_bancaria': '987654321',
        'tipo_cuenta': 'AHORROS',
        'banco': 'Davivienda'
    },
    {
        'id_trabajador': '1087654321',
        'tipo_documento': 'CC',
        'nombres': 'Juan Pablo',
        'apellidos': 'Ramírez Silva',
        'fecha_expedicion_doc': date(2014, 1, 10),
        'lugar_expedicion': 'Envigado',
        'nacionalidad': 'Colombiana',
        'fecha_nacimiento': date(1990, 7, 14),
        'lugar_nacimiento': 'Envigado',
        'genero': 'M',
        'estado_civil': 'UNION_LIBRE',
        'direccion_residencia': 'Calle 30 Sur #48-20',
        'ciudad_residencia': 'Envigado',
        'departamento_residencia': 'Antioquia',
        'telefono_celular': '3126789012',
        'correo_personal': 'juan.ramirez@email.com',
        'grupo_sanguineo_rh': 'B+',
        'nombres_padre': 'Pedro Ramírez',
        'nombres_madre': 'Luz Silva',
        'nombre_contacto_emergencia': 'Carolina Pérez (Compañera)',
        'numero_contacto_emergencia': '3145678901',
        'numero_hijos': 1,
        'cuenta_bancaria': '456789123',
        'tipo_cuenta': 'AHORROS',
        'banco': 'Banco de Bogotá'
    },
    {
        'id_trabajador': '1034567890',
        'tipo_documento': 'CC',
        'nombres': 'Diana Carolina',
        'apellidos': 'García Hernández',
        'fecha_expedicion_doc': date(2017, 5, 18),
        'lugar_expedicion': 'Itagüí',
        'nacionalidad': 'Colombiana',
        'fecha_nacimiento': date(1997, 2, 25),
        'lugar_nacimiento': 'Itagüí',
        'genero': 'F',
        'estado_civil': 'SOLTERA',
        'direccion_residencia': 'Carrera 52 #40-15',
        'ciudad_residencia': 'Itagüí',
        'departamento_residencia': 'Antioquia',
        'telefono_celular': '3187890123',
        'correo_personal': 'diana.garcia@email.com',
        'grupo_sanguineo_rh': 'AB+',
        'nombres_padre': 'Luis García',
        'nombres_madre': 'Patricia Hernández',
        'nombre_contacto_emergencia': 'Patricia Hernández (Madre)',
        'numero_contacto_emergencia': '3023456789',
        'numero_hijos': 0,
        'cuenta_bancaria': '789123456',
        'tipo_cuenta': 'AHORROS',
        'banco': 'Bancolombia'
    },
    {
        'id_trabajador': '1045678901',
        'tipo_documento': 'CC',
        'nombres': 'Luis Fernando',
        'apellidos': 'Moreno Castro',
        'fecha_expedicion_doc': date(2013, 9, 30),
        'lugar_expedicion': 'Medellín',
        'nacionalidad': 'Colombiana',
        'fecha_nacimiento': date(1988, 12, 5),
        'lugar_nacimiento': 'Medellín',
        'genero': 'M',
        'estado_civil': 'CASADO',
        'direccion_residencia': 'Calle 10 #20-30',
        'ciudad_residencia': 'Medellín',
        'departamento_residencia': 'Antioquia',
        'telefono_celular': '3199012345',
        'correo_personal': 'luis.moreno@email.com',
        'grupo_sanguineo_rh': 'O-',
        'nombres_padre': 'Roberto Moreno',
        'nombres_madre': 'Gloria Castro',
        'nombre_contacto_emergencia': 'Andrea Moreno (Esposa)',
        'numero_contacto_emergencia': '3167890123',
        'numero_hijos': 3,
        'cuenta_bancaria': '321654987',
        'tipo_cuenta': 'AHORROS',
        'banco': 'Davivienda'
    },
    {
        'id_trabajador': '79456123',
        'tipo_documento': 'CC',
        'nombres': 'Sofía',
        'apellidos': 'Pérez Álvarez',
        'fecha_expedicion_doc': date(2018, 4, 12),
        'lugar_expedicion': 'Medellín',
        'nacionalidad': 'Colombiana',
        'fecha_nacimiento': date(1999, 8, 30),
        'lugar_nacimiento': 'Sabaneta',
        'genero': 'F',
        'estado_civil': 'SOLTERA',
        'direccion_residencia': 'Carrera 43A #25-50',
        'ciudad_residencia': 'Sabaneta',
        'departamento_residencia': 'Antioquia',
        'telefono_celular': '3101234568',
        'correo_personal': 'sofia.perez@email.com',
        'grupo_sanguineo_rh': 'A-',
        'nombres_padre': 'Andrés Pérez',
        'nombres_madre': 'Claudia Álvarez',
        'nombre_contacto_emergencia': 'Claudia Álvarez (Madre)',
        'numero_contacto_emergencia': '3045678912',
        'numero_hijos': 0,
        'cuenta_bancaria': '654987321',
        'tipo_cuenta': 'AHORROS',
        'banco': 'BBVA'
    },
    {
        'id_trabajador': '1056789012',
        'tipo_documento': 'CC',
        'nombres': 'Miguel Ángel',
        'apellidos': 'Torres Ruiz',
        'fecha_expedicion_doc': date(2012, 11, 20),
        'lugar_expedicion': 'Copacabana',
        'nacionalidad': 'Colombiana',
        'fecha_nacimiento': date(1987, 4, 18),
        'lugar_nacimiento': 'Copacabana',
        'genero': 'M',
        'estado_civil': 'DIVORCIADO',
        'direccion_residencia': 'Calle 50 #70-10',
        'ciudad_residencia': 'Copacabana',
        'departamento_residencia': 'Antioquia',
        'telefono_celular': '3112345679',
        'correo_personal': 'miguel.torres@email.com',
        'grupo_sanguineo_rh': 'B-',
        'nombres_padre': 'Carlos Torres',
        'nombres_madre': 'Elena Ruiz',
        'nombre_contacto_emergencia': 'Elena Ruiz (Madre)',
        'numero_contacto_emergencia': '3056789123',
        'numero_hijos': 1,
        'cuenta_bancaria': '159753486',
        'tipo_cuenta': 'AHORROS',
        'banco': 'Banco de Bogotá'
    },
    {
        'id_trabajador': '52341678',
        'tipo_documento': 'CC',
        'nombres': 'Laura Daniela',
        'apellidos': 'Jiménez Ospina',
        'fecha_expedicion_doc': date(2016, 6, 8),
        'lugar_expedicion': 'La Estrella',
        'nacionalidad': 'Colombiana',
        'fecha_nacimiento': date(1994, 10, 22),
        'lugar_nacimiento': 'La Estrella',
        'genero': 'F',
        'estado_civil': 'UNION_LIBRE',
        'direccion_residencia': 'Carrera 60 #30-20',
        'ciudad_residencia': 'La Estrella',
        'departamento_residencia': 'Antioquia',
        'telefono_celular': '3123456780',
        'correo_personal': 'laura.jimenez@email.com',
        'grupo_sanguineo_rh': 'O+',
        'nombres_padre': 'Jorge Jiménez',
        'nombres_madre': 'Rosa Ospina',
        'nombre_contacto_emergencia': 'Pablo Gómez (Compañero)',
        'numero_contacto_emergencia': '3067890234',
        'numero_hijos': 1,
        'cuenta_bancaria': '753159486',
        'tipo_cuenta': 'AHORROS',
        'banco': 'Bancolombia'
    },
    {
        'id_trabajador': '1067890123',
        'tipo_documento': 'CC',
        'nombres': 'Andrés Felipe',
        'apellidos': 'Valencia Múnera',
        'fecha_expedicion_doc': date(2015, 2, 28),
        'lugar_expedicion': 'Caldas',
        'nacionalidad': 'Colombiana',
        'fecha_nacimiento': date(1991, 9, 12),
        'lugar_nacimiento': 'Caldas',
        'genero': 'M',
        'estado_civil': 'CASADO',
        'direccion_residencia': 'Calle 35 #55-40',
        'ciudad_residencia': 'Caldas',
        'departamento_residencia': 'Antioquia',
        'telefono_celular': '3134567891',
        'correo_personal': 'andres.valencia@email.com',
        'grupo_sanguineo_rh': 'A+',
        'nombres_padre': 'Felipe Valencia',
        'nombres_madre': 'Martha Múnera',
        'nombre_contacto_emergencia': 'Luisa Valencia (Esposa)',
        'numero_contacto_emergencia': '3078901345',
        'numero_hijos': 2,
        'cuenta_bancaria': '852963741',
        'tipo_cuenta': 'CORRIENTE',
        'banco': 'Davivienda'
    },
    {
        'id_trabajador': '43567812',
        'tipo_documento': 'CE',
        'nombres': 'José Luis',
        'apellidos': 'Méndez Paredes',
        'fecha_expedicion_doc': date(2019, 7, 15),
        'lugar_expedicion': 'Medellín',
        'nacionalidad': 'Venezolana',
        'fecha_nacimiento': date(1993, 3, 8),
        'lugar_nacimiento': 'Caracas',
        'genero': 'M',
        'estado_civil': 'SOLTERO',
        'direccion_residencia': 'Carrera 70 #42-18',
        'ciudad_residencia': 'Medellín',
        'departamento_residencia': 'Antioquia',
        'telefono_celular': '3145678902',
        'correo_personal': 'jose.mendez@email.com',
        'grupo_sanguineo_rh': 'O+',
        'nombres_padre': 'Luis Méndez',
        'nombres_madre': 'Carmen Paredes',
        'nombre_contacto_emergencia': 'Carmen Paredes (Madre)',
        'numero_contacto_emergencia': '3089012456',
        'numero_hijos': 0,
        'cuenta_bancaria': '951357486',
        'tipo_cuenta': 'AHORROS',
        'banco': 'BBVA'
    }
]

# ============================================================================
# 2. DATOS DE 5 TIPOS DE EPP (TipoDotacion)
# ============================================================================

tipos_dotacion_data = [
    {
        'nombre_tipo_dotacion': 'Casco de Seguridad',
        'vida_util_dias': 365,  # 1 año
        'descripcion': 'Casco de seguridad industrial clase G, protección contra impactos y descargas eléctricas',
        'requiere_talla': False,
        'tallas_disponibles': None,
        'normativa_referencia': 'ANSI Z89.1, Resolución 2400 de 1979',
        'activo': True
    },
    {
        'nombre_tipo_dotacion': 'Botas de Seguridad',
        'vida_util_dias': 365,  # 1 año
        'descripcion': 'Botas de seguridad con puntera de acero, antideslizantes y dieléctricas',
        'requiere_talla': True,
        'tallas_disponibles': '36,37,38,39,40,41,42,43,44,45',
        'normativa_referencia': 'ASTM F2413-18, Resolución 2400 de 1979',
        'activo': True
    },
    {
        'nombre_tipo_dotacion': 'Guantes de Seguridad',
        'vida_util_dias': 180,  # 6 meses
        'descripcion': 'Guantes de cuero reforzado para trabajo con elementos pesados y construcción',
        'requiere_talla': True,
        'tallas_disponibles': 'S,M,L,XL',
        'normativa_referencia': 'EN 388, Resolución 2400 de 1979',
        'activo': True
    },
    {
        'nombre_tipo_dotacion': 'Arnés de Seguridad',
        'vida_util_dias': 730,  # 2 años
        'descripcion': 'Arnés de cuerpo completo para trabajo en alturas con certificación vigente',
        'requiere_talla': True,
        'tallas_disponibles': 'S,M,L,XL',
        'normativa_referencia': 'Resolución 1409 de 2012 - Trabajo en Alturas',
        'activo': True
    },
    {
        'nombre_tipo_dotacion': 'Gafas de Seguridad',
        'vida_util_dias': 365,  # 1 año
        'descripcion': 'Gafas de seguridad con protección UV y anti-empañante para protección ocular',
        'requiere_talla': False,
        'tallas_disponibles': None,
        'normativa_referencia': 'ANSI Z87.1, Resolución 2400 de 1979',
        'activo': True
    }
]

# ============================================================================
# 3. DATOS DE 3 TIPOS DE CURSOS (TipoCurso)
# ============================================================================

tipos_curso_data = [
    {
        'nombre_tipo_curso': 'Trabajo Seguro en Alturas - Avanzado',
        'vigencia_dias': 365,  # 1 año
        'requiere_renovacion': True,
        'normativa_referencia': 'Resolución 1409 de 2012 - Ministerio del Trabajo',
        'dias_alerta_anticipada': 30,
        'descripcion': 'Curso avanzado de trabajo seguro en alturas para personal que realiza trabajos a más de 1.5 metros de altura. Incluye uso de arnés, líneas de vida y rescate.',
        'activo': True
    },
    {
        'nombre_tipo_curso': 'Manejo Seguro de Herramientas Eléctricas',
        'vigencia_dias': 730,  # 2 años
        'requiere_renovacion': True,
        'normativa_referencia': 'RETIE - Reglamento Técnico de Instalaciones Eléctricas',
        'dias_alerta_anticipada': 60,
        'descripcion': 'Capacitación en el uso seguro de herramientas eléctricas, prevención de riesgos eléctricos y primeros auxilios en caso de electrocución.',
        'activo': True
    },
    {
        'nombre_tipo_curso': 'Seguridad y Salud en el Trabajo - SG-SST',
        'vigencia_dias': 1095,  # 3 años
        'requiere_renovacion': True,
        'normativa_referencia': 'Decreto 1072 de 2015 - Sistema de Gestión SST',
        'dias_alerta_anticipada': 90,
        'descripcion': 'Curso integral del Sistema de Gestión de Seguridad y Salud en el Trabajo. Incluye identificación de peligros, evaluación de riesgos y medidas de control.',
        'activo': True
    }
]

# ============================================================================
# 4. DATOS DE 5 TIPOS DE DOCUMENTOS (TipoDocumento)
# ============================================================================

tipos_documento_data = [
    {
        'nombre_tipo_documento': 'Fotocopia Cédula de Ciudadanía',
        'descripcion': 'Fotocopia legible de la cédula de ciudadanía por ambas caras',
        'es_obligatorio': True,
        'requiere_vigencia': False,
        'icono_bootstrap': 'bi-card-text',
        'orden_visualizacion': 1,
        'activo': True
    },
    {
        'nombre_tipo_documento': 'Certificado de Afiliación EPS',
        'descripcion': 'Certificado vigente de afiliación a Entidad Promotora de Salud',
        'es_obligatorio': True,
        'requiere_vigencia': True,
        'icono_bootstrap': 'bi-hospital',
        'orden_visualizacion': 2,
        'activo': True
    },
    {
        'nombre_tipo_documento': 'Certificado de Afiliación ARL',
        'descripcion': 'Certificado vigente de afiliación a Administradora de Riesgos Laborales',
        'es_obligatorio': True,
        'requiere_vigencia': True,
        'icono_bootstrap': 'bi-shield-check',
        'orden_visualizacion': 3,
        'activo': True
    },
    {
        'nombre_tipo_documento': 'Certificado de Antecedentes',
        'descripcion': 'Certificado de antecedentes judiciales, fiscales y disciplinarios',
        'es_obligatorio': False,
        'requiere_vigencia': True,
        'icono_bootstrap': 'bi-file-earmark-check',
        'orden_visualizacion': 4,
        'activo': True
    },
    {
        'nombre_tipo_documento': 'Hoja de Vida',
        'descripcion': 'Formato de hoja de vida con experiencia laboral y estudios realizados',
        'es_obligatorio': True,
        'requiere_vigencia': False,
        'icono_bootstrap': 'bi-person-vcard',
        'orden_visualizacion': 5,
        'activo': True
    }
]

# ============================================================================
# EJEMPLO DE SCRIPT PARA INSERTAR LOS DATOS EN DJANGO
# ============================================================================

def insertar_datos_ejemplo():
    """
    Script de ejemplo para insertar los datos usando Django ORM.
    Ejecutar en Django shell: python manage.py shell
    Luego: exec(open('datos_prueba_american_carpas.py').read())
    Finalmente: insertar_datos_ejemplo()
    """
    
    from trabajadores.models import (
        TrabajadorPersonal, TipoDotacion, TipoCurso, TipoDocumento
    )
    
    print("=" * 80)
    print("INSERTANDO DATOS DE PRUEBA - AMERICAN CARPAS")
    print("=" * 80)
    
    # 1. Insertar Tipos de Dotación (EPP)
    print("\n1. Insertando Tipos de Dotación (EPP)...")
    for tipo_data in tipos_dotacion_data:
        tipo, created = TipoDotacion.objects.get_or_create(
            nombre_tipo_dotacion=tipo_data['nombre_tipo_dotacion'],
            defaults=tipo_data
        )
        if created:
            print(f"   ✓ Creado: {tipo.nombre_tipo_dotacion}")
        else:
            print(f"   → Ya existe: {tipo.nombre_tipo_dotacion}")
    
    # 2. Insertar Tipos de Curso
    print("\n2. Insertando Tipos de Curso...")
    for curso_data in tipos_curso_data:
        curso, created = TipoCurso.objects.get_or_create(
            nombre_tipo_curso=curso_data['nombre_tipo_curso'],
            defaults=curso_data
        )
        if created:
            print(f"   ✓ Creado: {curso.nombre_tipo_curso}")
        else:
            print(f"   → Ya existe: {curso.nombre_tipo_curso}")
    
    # 3. Insertar Tipos de Documento
    print("\n3. Insertando Tipos de Documento...")
    for doc_data in tipos_documento_data:
        doc, created = TipoDocumento.objects.get_or_create(
            nombre_tipo_documento=doc_data['nombre_tipo_documento'],
            defaults=doc_data
        )
        if created:
            print(f"   ✓ Creado: {doc.nombre_tipo_documento}")
        else:
            print(f"   → Ya existe: {doc.nombre_tipo_documento}")
    
    # 4. Insertar Trabajadores
    print("\n4. Insertando Trabajadores...")
    for trab_data in trabajadores_data:
        trabajador, created = TrabajadorPersonal.objects.get_or_create(
            id_trabajador=trab_data['id_trabajador'],
            defaults=trab_data
        )
        if created:
            print(f"   ✓ Creado: {trabajador.nombres} {trabajador.apellidos}")
        else:
            print(f"   → Ya existe: {trabajador.nombres} {trabajador.apellidos}")
    
    print("\n" + "=" * 80)
    print("RESUMEN DE DATOS INSERTADOS:")
    print("=" * 80)
    print(f"Tipos de Dotación (EPP): {TipoDotacion.objects.count()}")
    print(f"Tipos de Curso: {TipoCurso.objects.count()}")
    print(f"Tipos de Documento: {TipoDocumento.objects.count()}")
    print(f"Trabajadores: {TrabajadorPersonal.objects.count()}")
    print("=" * 80)
    print("✓ Proceso completado exitosamente!")
    print("=" * 80)

# ============================================================================
# INSTRUCCIONES DE USO
# ============================================================================

"""
CÓMO USAR ESTE ARCHIVO:

OPCIÓN 1 - Django Shell:
-----------------------
1. Guardar este archivo en el directorio raíz de tu proyecto Django
2. Abrir terminal y ejecutar:
   python manage.py shell
   
3. En el shell de Django ejecutar:
   exec(open('datos_prueba_american_carpas.py').read())
   insertar_datos_ejemplo()

OPCIÓN 2 - Script de Management Command:
---------------------------------------
Crear un archivo en: trabajadores/management/commands/cargar_datos_prueba.py
Y copiar la función insertar_datos_ejemplo() allí

Luego ejecutar:
python manage.py cargar_datos_prueba

OPCIÓN 3 - Fixtures JSON:
------------------------
Convertir estos datos a formato JSON de fixtures y usar:
python manage.py loaddata datos_prueba.json

NOTA: Asegúrate de que el nombre de tu app sea 'trabajadores' o ajusta
      los imports según el nombre de tu aplicación.
"""
