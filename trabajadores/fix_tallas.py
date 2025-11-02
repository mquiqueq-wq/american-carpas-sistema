# Script de diagnóstico y corrección para tallas
# Ejecutar en Django shell: python manage.py shell < fix_tallas.py

from trabajadores.models import TipoDotacion

print("=" * 60)
print("DIAGNÓSTICO DE TALLAS EN TIPOS DE DOTACIÓN")
print("=" * 60)

for tipo in TipoDotacion.objects.all():
    print(f"\n📦 Tipo: {tipo.nombre_tipo_dotacion}")
    print(f"   ID: {tipo.id_tipo_dotacion}")
    print(f"   Requiere talla: {tipo.requiere_talla}")
    print(f"   Tallas guardadas (raw): '{tipo.tallas_disponibles}'")
    
    if tipo.requiere_talla and tipo.tallas_disponibles:
        tallas_lista = tipo.get_tallas_lista()
        print(f"   Tallas procesadas: {tallas_lista}")
        print(f"   Número de tallas: {len(tallas_lista)}")
        
        # Verificar si hay espacios o caracteres extraños
        for i, talla in enumerate(tallas_lista):
            repr_talla = repr(talla)  # Muestra espacios y caracteres especiales
            print(f"      [{i}] {repr_talla} (len={len(talla)})")

print("\n" + "=" * 60)
print("PRUEBA DE VALIDACIÓN")
print("=" * 60)

# Buscar el tipo "Botas de Seguridad"
try:
    botas = TipoDotacion.objects.get(nombre_tipo_dotacion__icontains="botas")
    print(f"\n✓ Encontrado: {botas.nombre_tipo_dotacion}")
    print(f"  Tallas: {botas.get_tallas_lista()}")
    
    # Probar validación con diferentes formatos
    test_tallas = ['30', ' 30', '30 ', ' 30 ', '35', '40']
    for test in test_tallas:
        es_valida = botas.es_talla_valida(test)
        print(f"  ¿'{test}' es válida? {es_valida}")
        
except TipoDotacion.DoesNotExist:
    print("\n❌ No se encontró tipo de dotación 'Botas'")

print("\n" + "=" * 60)
print("CORRECCIÓN AUTOMÁTICA")
print("=" * 60)

# Limpiar todas las tallas con espacios
for tipo in TipoDotacion.objects.filter(requiere_talla=True):
    if tipo.tallas_disponibles:
        original = tipo.tallas_disponibles
        # Limpiar cada talla individualmente y reunir
        tallas = [t.strip() for t in original.split(',')]
        tallas_limpias = [t for t in tallas if t]  # Eliminar vacíos
        nuevo_valor = ','.join(tallas_limpias)
        
        if original != nuevo_valor:
            print(f"\n🔧 Corrigiendo: {tipo.nombre_tipo_dotacion}")
            print(f"   ANTES: '{original}'")
            print(f"   DESPUÉS: '{nuevo_valor}'")
            tipo.tallas_disponibles = nuevo_valor
            tipo.save()
            print(f"   ✓ Guardado")
        else:
            print(f"\n✓ OK: {tipo.nombre_tipo_dotacion}")

print("\n" + "=" * 60)
print("FINALIZADO")
print("=" * 60)
