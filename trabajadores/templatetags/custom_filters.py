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
def abs_value(value):
    """
    Retorna el valor absoluto de un número.
    Ejemplo: -5 -> 5
    """
    try:
        return abs(int(value))
    except (ValueError, TypeError):
        return value