from django import template

register = template.Library()

@register.filter
def attr(obj, name):
    return getattr(obj, name, '')

@register.filter
def get_item(d, key):
    try:
        return d.get(key)
    except Exception:
        return ''

@register.filter(name='currency')
def currency(value):
    """
    Formatea un número como moneda colombiana.
    Ejemplo: 1500000 -> $1.500.000
    """
    try:
        # Convertir a float y formatear
        value = float(value)
        # Formatear con separador de miles
        formatted = "${:,.0f}".format(value)
        # Reemplazar coma por punto (formato colombiano)
        formatted = formatted.replace(",", ".")
        return formatted
    except (ValueError, TypeError):
        return value

@register.filter(name='abs')
def absolute_value(value):
    """
    Retorna el valor absoluto de un número.
    Ejemplo: -5 -> 5
    
    Nombre de función diferente para evitar conflictos con abs() nativo
    """
    try:
        # Convertir a entero y obtener valor absoluto
        num = int(value)
        if num < 0:
            return -num
        return num
    except (ValueError, TypeError):
        return 0

@register.filter
def filter_vencidos(documentos):
    """Filtra documentos vencidos"""
    vencidos = []
    for doc in documentos:
        if doc.tipo_documento.requiere_vigencia:
            dias = doc.dias_para_vencer()
            if dias is not None and dias < 0:
                vencidos.append(doc)
    return vencidos

@register.filter
def filter_proximos_vencer(documentos):
    """Filtra documentos próximos a vencer (30 días)"""
    proximos = []
    for doc in documentos:
        if doc.tipo_documento.requiere_vigencia:
            dias = doc.dias_para_vencer()
            if dias is not None and 0 <= dias <= 30:
                proximos.append(doc)
    return proximos