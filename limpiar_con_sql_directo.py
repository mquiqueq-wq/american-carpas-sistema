"""
Script para limpiar todas las tablas de proveedores usando conexión directa a MySQL
Ejecutar desde la raíz del proyecto: python limpiar_con_sql_directo.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'american_carpas.settings')
django.setup()

# Importar la configuración de la base de datos
from django.conf import settings
from django.db import connection

print("="*60)
print("LIMPIANDO TABLAS DE PROVEEDORES CON SQL DIRECTO")
print("="*60)
print()

# Confirmar acción
respuesta = input("¿Estás seguro de que quieres borrar TODOS los datos de proveedores? (escribe 'SI' para confirmar): ")

if respuesta.upper() == 'SI':
    print()
    print("Conectando a la base de datos...")
    
    try:
        with connection.cursor() as cursor:
            # Desactivar verificación de llaves foráneas
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            print("✓ Llaves foráneas desactivadas temporalmente")
            
            # Limpiar todas las tablas
            tablas = [
                'productos_servicios_proveedores',
                'documentos_proveedores',
                'contactos_proveedores',
                'proveedores',
                'tipos_documentos_proveedores',
                'categorias_proveedores',
                'tipos_proveedores'
            ]
            
            print()
            print("Limpiando tablas...")
            for tabla in tablas:
                try:
                    cursor.execute(f"TRUNCATE TABLE {tabla};")
                    print(f"✓ Tabla '{tabla}' limpiada")
                except Exception as e:
                    print(f"⚠ Error al limpiar '{tabla}': {e}")
            
            # Reactivar verificación de llaves foráneas
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            print()
            print("✓ Llaves foráneas reactivadas")
        
        print()
        print("="*60)
        print("✅ TODAS LAS TABLAS HAN SIDO LIMPIADAS EXITOSAMENTE!")
        print("="*60)
        print()
        print("PRÓXIMOS PASOS:")
        print()
        print("1. Ejecutar: python manage.py makemigrations proveedores")
        print()
        print("2. Cuando pregunte por default, responder:")
        print("   Select an option: 1")
        print("   Please enter the default value: timezone.now()")
        print()
        print("3. Ejecutar: python manage.py migrate")
        print()
        
    except Exception as e:
        print()
        print("="*60)
        print("❌ ERROR AL LIMPIAR LAS TABLAS")
        print("="*60)
        print(f"Error: {e}")
        print()
        print("Verifica que:")
        print("- MySQL esté corriendo")
        print("- La configuración de BD en settings.py sea correcta")
        print()

else:
    print()
    print("❌ Operación cancelada. No se borró ningún dato.")
    print()
