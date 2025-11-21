# -*- coding: utf-8 -*-
"""
Management command para cargar datos de prueba en la base de datos
Uso: python manage.py cargar_datos_prueba
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import date
from trabajadores.models import (
    TrabajadorPersonal, TipoDotacion, TipoCurso, TipoDocumento
)


class Command(BaseCommand):
    help = 'Carga datos de prueba en la base de datos de American Carpas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Fuerza la carga incluso si ya existen datos',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(self.style.SUCCESS('CARGANDO DATOS DE PRUEBA - AMERICAN CARPAS'))
        self.stdout.write(self.style.SUCCESS('=' * 80))

        # Verificar si ya hay datos
        if not options['force']:
            if TrabajadorPersonal.objects.exists():
                self.stdout.write(self.style.WARNING(
                    '\nYa existen trabajadores en la base de datos.'
                ))
                self.stdout.write(self.style.WARNING(
                    'Use --force para cargar de todas formas.'
                ))
                return

        try:
            with transaction.atomic():
                self.cargar_tipos_dotacion()
                self.cargar_tipos_curso()
                self.cargar_tipos_documento()
                self.cargar_trabajadores()
                
            self.mostrar_resumen()
            self.stdout.write(self.style.SUCCESS('\n✓ Datos cargados exitosamente!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error al cargar datos: {str(e)}'))
            raise

    def cargar_tipos_dotacion(self):
        self.stdout.write('\n1. Cargando Tipos de Dotacion (EPP)...')
        
        datos = [
            {
                'nombre_tipo_dotacion': 'Casco de Seguridad',
                'vida_util_dias': 365,
                'descripcion': 'Casco de seguridad industrial clase G, proteccion contra impactos y descargas electricas',
                'requiere_talla': False,
                'tallas_disponibles': None,
                'normativa_referencia': 'ANSI Z89.1, Resolucion 2400 de 1979',
                'activo': True
            },
            {
                'nombre_tipo_dotacion': 'Botas de Seguridad',
                'vida_util_dias': 365,
                'descripcion': 'Botas de seguridad con puntera de acero, antideslizantes y dielectricas',
                'requiere_talla': True,
                'tallas_disponibles': '36,37,38,39,40,41,42,43,44,45',
                'normativa_referencia': 'ASTM F2413-18, Resolucion 2400 de 1979',
                'activo': True
            },
            {
                'nombre_tipo_dotacion': 'Guantes de Seguridad',
                'vida_util_dias': 180,
                'descripcion': 'Guantes de cuero reforzado para trabajo con elementos pesados y construccion',
                'requiere_talla': True,
                'tallas_disponibles': 'S,M,L,XL',
                'normativa_referencia': 'EN 388, Resolucion 2400 de 1979',
                'activo': True
            },
            {
                'nombre_tipo_dotacion': 'Arnes de Seguridad',
                'vida_util_dias': 730,
                'descripcion': 'Arnes de cuerpo completo para trabajo en alturas con certificacion vigente',
                'requiere_talla': True,
                'tallas_disponibles': 'S,M,L,XL',
                'normativa_referencia': 'Resolucion 1409 de 2012 - Trabajo en Alturas',
                'activo': True
            },
            {
                'nombre_tipo_dotacion': 'Gafas de Seguridad',
                'vida_util_dias': 365,
                'descripcion': 'Gafas de seguridad con proteccion UV y anti-empanante para proteccion ocular',
                'requiere_talla': False,
                'tallas_disponibles': None,
                'normativa_referencia': 'ANSI Z87.1, Resolucion 2400 de 1979',
                'activo': True
            }
        ]

        for item in datos:
            obj, created = TipoDotacion.objects.get_or_create(
                nombre_tipo_dotacion=item['nombre_tipo_dotacion'],
                defaults=item
            )
            status = '✓ Creado' if created else '→ Ya existe'
            self.stdout.write(f'   {status}: {obj.nombre_tipo_dotacion}')

    def cargar_tipos_curso(self):
        self.stdout.write('\n2. Cargando Tipos de Curso...')
        
        datos = [
            {
                'nombre_tipo_curso': 'Trabajo Seguro en Alturas - Avanzado',
                'vigencia_dias': 365,
                'requiere_renovacion': True,
                'normativa_referencia': 'Resolucion 1409 de 2012 - Ministerio del Trabajo',
                'dias_alerta_anticipada': 30,
                'descripcion': 'Curso avanzado de trabajo seguro en alturas para personal que realiza trabajos a mas de 1.5 metros de altura.',
                'activo': True
            },
            {
                'nombre_tipo_curso': 'Manejo Seguro de Herramientas Electricas',
                'vigencia_dias': 730,
                'requiere_renovacion': True,
                'normativa_referencia': 'RETIE - Reglamento Tecnico de Instalaciones Electricas',
                'dias_alerta_anticipada': 60,
                'descripcion': 'Capacitacion en el uso seguro de herramientas electricas y prevencion de riesgos electricos.',
                'activo': True
            },
            {
                'nombre_tipo_curso': 'Seguridad y Salud en el Trabajo - SG-SST',
                'vigencia_dias': 1095,
                'requiere_renovacion': True,
                'normativa_referencia': 'Decreto 1072 de 2015 - Sistema de Gestion SST',
                'dias_alerta_anticipada': 90,
                'descripcion': 'Curso integral del Sistema de Gestion de Seguridad y Salud en el Trabajo.',
                'activo': True
            }
        ]

        for item in datos:
            obj, created = TipoCurso.objects.get_or_create(
                nombre_tipo_curso=item['nombre_tipo_curso'],
                defaults=item
            )
            status = '✓ Creado' if created else '→ Ya existe'
            self.stdout.write(f'   {status}: {obj.nombre_tipo_curso}')

    def cargar_tipos_documento(self):
        self.stdout.write('\n3. Cargando Tipos de Documento...')
        
        datos = [
            {
                'nombre_tipo_documento': 'Fotocopia Cedula de Ciudadania',
                'descripcion': 'Fotocopia legible de la cedula de ciudadania por ambas caras',
                'es_obligatorio': True,
                'requiere_vigencia': False,
                'icono_bootstrap': 'bi-card-text',
                'orden_visualizacion': 1,
                'activo': True
            },
            {
                'nombre_tipo_documento': 'Certificado de Afiliacion EPS',
                'descripcion': 'Certificado vigente de afiliacion a Entidad Promotora de Salud',
                'es_obligatorio': True,
                'requiere_vigencia': True,
                'icono_bootstrap': 'bi-hospital',
                'orden_visualizacion': 2,
                'activo': True
            },
            {
                'nombre_tipo_documento': 'Certificado de Afiliacion ARL',
                'descripcion': 'Certificado vigente de afiliacion a Administradora de Riesgos Laborales',
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

        for item in datos:
            obj, created = TipoDocumento.objects.get_or_create(
                nombre_tipo_documento=item['nombre_tipo_documento'],
                defaults=item
            )
            status = '✓ Creado' if created else '→ Ya existe'
            self.stdout.write(f'   {status}: {obj.nombre_tipo_documento}')

    def cargar_trabajadores(self):
        self.stdout.write('\n4. Cargando Trabajadores...')
        
        datos = [
            {
                'id_trabajador': '1098765432',
                'tipo_documento': 'CC',
                'nombres': 'Carlos Andres',
                'apellidos': 'Rodriguez Gomez',
                'fecha_expedicion_doc': date(2015, 3, 15),
                'lugar_expedicion': 'Medellin',
                'nacionalidad': 'Colombiana',
                'fecha_nacimiento': date(1992, 5, 20),
                'lugar_nacimiento': 'Medellin',
                'genero': 'M',
                'estado_civil': 'CASADO',
                'direccion_residencia': 'Calle 45 #23-15',
                'ciudad_residencia': 'Medellin',
                'departamento_residencia': 'Antioquia',
                'telefono_celular': '3201234567',
                'correo_personal': 'carlos.rodriguez@email.com',
                'grupo_sanguineo_rh': 'O+',
                'nombres_padre': 'Jose Rodriguez',
                'nombres_madre': 'Maria Gomez',
                'nombre_contacto_emergencia': 'Ana Rodriguez (Esposa)',
                'numero_contacto_emergencia': '3109876543',
                'numero_hijos': 2,
                'cuenta_bancaria': '123456789',
                'tipo_cuenta': 'AHORROS',
                'banco': 'Bancolombia'
            },
            {
                'id_trabajador': '1023456789',
                'tipo_documento': 'CC',
                'nombres': 'Maria Fernanda',
                'apellidos': 'Lopez Martinez',
                'fecha_expedicion_doc': date(2016, 8, 22),
                'lugar_expedicion': 'Bello',
                'nacionalidad': 'Colombiana',
                'fecha_nacimiento': date(1995, 11, 8),
                'lugar_nacimiento': 'Bello',
                'genero': 'F',
                'estado_civil': 'SOLTERO',
                'direccion_residencia': 'Carrera 80 #50-30 Apto 402',
                'ciudad_residencia': 'Medellin',
                'departamento_residencia': 'Antioquia',
                'telefono_celular': '3154567890',
                'correo_personal': 'maria.lopez@email.com',
                'grupo_sanguineo_rh': 'A+',
                'nombres_padre': 'Fernando Lopez',
                'nombres_madre': 'Sandra Martinez',
                'nombre_contacto_emergencia': 'Sandra Martinez (Madre)',
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
                'apellidos': 'Ramirez Silva',
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
                'nombres_padre': 'Pedro Ramirez',
                'nombres_madre': 'Luz Silva',
                'nombre_contacto_emergencia': 'Carolina Perez (Companera)',
                'numero_contacto_emergencia': '3145678901',
                'numero_hijos': 1,
                'cuenta_bancaria': '456789123',
                'tipo_cuenta': 'AHORROS',
                'banco': 'Banco de Bogota'
            },
            {
                'id_trabajador': '1034567890',
                'tipo_documento': 'CC',
                'nombres': 'Diana Carolina',
                'apellidos': 'Garcia Hernandez',
                'fecha_expedicion_doc': date(2017, 5, 18),
                'lugar_expedicion': 'Itagui',
                'nacionalidad': 'Colombiana',
                'fecha_nacimiento': date(1997, 2, 25),
                'lugar_nacimiento': 'Itagui',
                'genero': 'F',
                'estado_civil': 'SOLTERO',
                'direccion_residencia': 'Carrera 52 #40-15',
                'ciudad_residencia': 'Itagui',
                'departamento_residencia': 'Antioquia',
                'telefono_celular': '3187890123',
                'correo_personal': 'diana.garcia@email.com',
                'grupo_sanguineo_rh': 'AB+',
                'nombres_padre': 'Luis Garcia',
                'nombres_madre': 'Patricia Hernandez',
                'nombre_contacto_emergencia': 'Patricia Hernandez (Madre)',
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
                'lugar_expedicion': 'Medellin',
                'nacionalidad': 'Colombiana',
                'fecha_nacimiento': date(1988, 12, 5),
                'lugar_nacimiento': 'Medellin',
                'genero': 'M',
                'estado_civil': 'CASADO',
                'direccion_residencia': 'Calle 10 #20-30',
                'ciudad_residencia': 'Medellin',
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
                'nombres': 'Sofia',
                'apellidos': 'Perez Alvarez',
                'fecha_expedicion_doc': date(2018, 4, 12),
                'lugar_expedicion': 'Medellin',
                'nacionalidad': 'Colombiana',
                'fecha_nacimiento': date(1999, 8, 30),
                'lugar_nacimiento': 'Sabaneta',
                'genero': 'F',
                'estado_civil': 'SOLTERO',
                'direccion_residencia': 'Carrera 43A #25-50',
                'ciudad_residencia': 'Sabaneta',
                'departamento_residencia': 'Antioquia',
                'telefono_celular': '3101234568',
                'correo_personal': 'sofia.perez@email.com',
                'grupo_sanguineo_rh': 'A-',
                'nombres_padre': 'Andres Perez',
                'nombres_madre': 'Claudia Alvarez',
                'nombre_contacto_emergencia': 'Claudia Alvarez (Madre)',
                'numero_contacto_emergencia': '3045678912',
                'numero_hijos': 0,
                'cuenta_bancaria': '654987321',
                'tipo_cuenta': 'AHORROS',
                'banco': 'BBVA'
            },
            {
                'id_trabajador': '1056789012',
                'tipo_documento': 'CC',
                'nombres': 'Miguel Angel',
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
                'banco': 'Banco de Bogota'
            },
            {
                'id_trabajador': '52341678',
                'tipo_documento': 'CC',
                'nombres': 'Laura Daniela',
                'apellidos': 'Jimenez Ospina',
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
                'nombres_padre': 'Jorge Jimenez',
                'nombres_madre': 'Rosa Ospina',
                'nombre_contacto_emergencia': 'Pablo Gomez (Companero)',
                'numero_contacto_emergencia': '3067890234',
                'numero_hijos': 1,
                'cuenta_bancaria': '753159486',
                'tipo_cuenta': 'AHORROS',
                'banco': 'Bancolombia'
            },
            {
                'id_trabajador': '1067890123',
                'tipo_documento': 'CC',
                'nombres': 'Andres Felipe',
                'apellidos': 'Valencia Munera',
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
                'nombres_madre': 'Martha Munera',
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
                'nombres': 'Jose Luis',
                'apellidos': 'Mendez Paredes',
                'fecha_expedicion_doc': date(2019, 7, 15),
                'lugar_expedicion': 'Medellin',
                'nacionalidad': 'Venezolana',
                'fecha_nacimiento': date(1993, 3, 8),
                'lugar_nacimiento': 'Caracas',
                'genero': 'M',
                'estado_civil': 'SOLTERO',
                'direccion_residencia': 'Carrera 70 #42-18',
                'ciudad_residencia': 'Medellin',
                'departamento_residencia': 'Antioquia',
                'telefono_celular': '3145678902',
                'correo_personal': 'jose.mendez@email.com',
                'grupo_sanguineo_rh': 'O+',
                'nombres_padre': 'Luis Mendez',
                'nombres_madre': 'Carmen Paredes',
                'nombre_contacto_emergencia': 'Carmen Paredes (Madre)',
                'numero_contacto_emergencia': '3089012456',
                'numero_hijos': 0,
                'cuenta_bancaria': '951357486',
                'tipo_cuenta': 'AHORROS',
                'banco': 'BBVA'
            }
        ]

        for item in datos:
            obj, created = TrabajadorPersonal.objects.get_or_create(
                id_trabajador=item['id_trabajador'],
                defaults=item
            )
            status = '✓ Creado' if created else '→ Ya existe'
            self.stdout.write(f'   {status}: {obj.nombres} {obj.apellidos}')

    def mostrar_resumen(self):
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 80))
        self.stdout.write(self.style.SUCCESS('RESUMEN DE DATOS:'))
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(f'Tipos de Dotacion (EPP): {TipoDotacion.objects.count()}')
        self.stdout.write(f'Tipos de Curso: {TipoCurso.objects.count()}')
        self.stdout.write(f'Tipos de Documento: {TipoDocumento.objects.count()}')
        self.stdout.write(f'Trabajadores: {TrabajadorPersonal.objects.count()}')
        self.stdout.write(self.style.SUCCESS('=' * 80))
