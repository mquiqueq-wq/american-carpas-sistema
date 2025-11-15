"""
Script para limpiar registros de archivos que no existen físicamente
Ejecutar desde la raíz del proyecto: python limpiar_archivos_huerfanos.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'american_carpas_project.settings')
django.setup()

from trabajadores.models import Trabajador, CursoTrabajador, DocumentoTrabajador
from proveedores.models import Proveedor, DocumentoProveedor

def limpiar_archivos_huerfanos():
    """
    Limpia referencias a archivos que no existen físicamente
    """
    
    print("="*60)
    print("🧹 LIMPIEZA DE ARCHIVOS HUÉRFANOS")
    print("="*60)
    
    total_limpiados = 0
    
    # =========================================================
    # LIMPIAR TRABAJADORES
    # =========================================================
    print("\n📋 Revisando TRABAJADORES...")
    for trabajador in Trabajador.objects.all():
        # Revisar foto
        if trabajador.foto and not trabajador.foto.storage.exists(trabajador.foto.name):
            print(f"  ❌ Trabajador {trabajador.numero_documento}: foto no existe")
            trabajador.foto = None
            trabajador.save()
            total_limpiados += 1
        
        # Revisar documento de identidad
        if trabajador.documento_identidad and not trabajador.documento_identidad.storage.exists(trabajador.documento_identidad.name):
            print(f"  ❌ Trabajador {trabajador.numero_documento}: documento de identidad no existe")
            trabajador.documento_identidad = None
            trabajador.save()
            total_limpiados += 1
    
    # =========================================================
    # LIMPIAR CURSOS DE TRABAJADORES
    # =========================================================
    print("\n📚 Revisando CURSOS DE TRABAJADORES...")
    for curso in CursoTrabajador.objects.all():
        if curso.certificado and not curso.certificado.storage.exists(curso.certificado.name):
            print(f"  ❌ Curso {curso.id_curso}: certificado no existe")
            curso.certificado = None
            curso.save()
            total_limpiados += 1
    
    # =========================================================
    # LIMPIAR DOCUMENTOS DE TRABAJADORES
    # =========================================================
    print("\n📄 Revisando DOCUMENTOS DE TRABAJADORES...")
    for doc in DocumentoTrabajador.objects.all():
        if doc.archivo and not doc.archivo.storage.exists(doc.archivo.name):
            print(f"  ❌ Documento {doc.id_documento}: archivo no existe")
            doc.archivo = None
            doc.save()
            total_limpiados += 1
    
    # =========================================================
    # LIMPIAR PROVEEDORES
    # =========================================================
    print("\n🏢 Revisando PROVEEDORES...")
    for proveedor in Proveedor.objects.all():
        if proveedor.logo and not proveedor.logo.storage.exists(proveedor.logo.name):
            print(f"  ❌ Proveedor {proveedor.razon_social}: logo no existe")
            proveedor.logo = None
            proveedor.save()
            total_limpiados += 1
    
    # =========================================================
    # LIMPIAR DOCUMENTOS DE PROVEEDORES
    # =========================================================
    print("\n📑 Revisando DOCUMENTOS DE PROVEEDORES...")
    for doc in DocumentoProveedor.objects.all():
        if doc.archivo and not doc.archivo.storage.exists(doc.archivo.name):
            print(f"  ❌ Documento {doc.id_documento}: archivo no existe")
            doc.archivo = None
            doc.save()
            total_limpiados += 1
    
    # =========================================================
    # RESUMEN
    # =========================================================
    print("\n" + "="*60)
    print(f"✅ LIMPIEZA COMPLETADA")
    print(f"🎯 Total de archivos huérfanos limpiados: {total_limpiados}")
    print("="*60)

if __name__ == '__main__':
    limpiar_archivos_huerfanos()
