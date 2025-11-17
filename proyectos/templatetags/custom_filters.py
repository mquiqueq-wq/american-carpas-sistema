"""
Filtros personalizados para templates del módulo de proyectos
American Carpas 1 SAS
"""

from django import template

register = template.Library()


@register.filter(name='abs')
def abs_filter(value):
    """
    Retorna el valor absoluto de un número.
    Uso en template: {{ numero|abs }}
    """
    try:
        return abs(value)
    except (ValueError, TypeError):
        return value


@register.filter(name='percentage')
def percentage(value, total):
    """
    Calcula el porcentaje de un valor respecto a un total.
    Uso en template: {{ valor|percentage:total }}
    """
    try:
        if total == 0:
            return 0
        return round((float(value) / float(total)) * 100, 2)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter(name='days_color')
def days_color(days):
    """
    Retorna una clase de color Bootstrap según los días restantes.
    Uso en template: {{ dias|days_color }}
    """
    try:
        days = int(days)
        if days < 0:
            return 'danger'  # Atrasado
        elif days <= 7:
            return 'warning'  # Próximo a vencer
        elif days <= 30:
            return 'info'  # Alerta temprana
        else:
            return 'success'  # A tiempo
    except (ValueError, TypeError):
        return 'secondary'


@register.filter(name='vigencia_badge')
def vigencia_badge(documento):
    """
    Retorna la clase de badge según la vigencia del documento.
    Uso en template: {{ documento|vigencia_badge }}
    """
    if not documento.tipo_documento.requiere_vigencia:
        return 'secondary'
    
    if not documento.fecha_vencimiento:
        return 'secondary'
    
    if documento.esta_vigente():
        dias = documento.dias_para_vencer()
        if dias is not None and dias <= documento.tipo_documento.dias_alerta_vencimiento:
            return 'warning'
        return 'success'
    else:
        return 'danger'


@register.filter(name='estado_badge_color')
def estado_badge_color(estado):
    """
    Retorna el color del badge según el estado del proyecto.
    Uso en template: {{ estado|estado_badge_color }}
    """
    if hasattr(estado, 'color_badge'):
        return estado.color_badge
    return 'secondary'


@register.filter(name='avance_color')
def avance_color(porcentaje):
    """
    Retorna una clase de color según el porcentaje de avance.
    Uso en template: {{ porcentaje|avance_color }}
    """
    try:
        porcentaje = float(porcentaje)
        if porcentaje == 0:
            return 'secondary'
        elif porcentaje < 25:
            return 'danger'
        elif porcentaje < 50:
            return 'warning'
        elif porcentaje < 75:
            return 'info'
        elif porcentaje < 100:
            return 'primary'
        else:
            return 'success'
    except (ValueError, TypeError):
        return 'secondary'


@register.filter(name='format_currency')
def format_currency(value):
    """
    Formatea un número como moneda colombiana.
    Uso en template: {{ valor|format_currency }}
    """
    try:
        value = float(value)
        return f"${value:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return "$0"


@register.filter(name='tipo_evidencia_icon')
def tipo_evidencia_icon(tipo):
    """
    Retorna el icono Bootstrap según el tipo de evidencia.
    Uso en template: {{ tipo|tipo_evidencia_icon }}
    """
    iconos = {
        'INICIO': 'bi-flag',
        'AVANCE': 'bi-graph-up',
        'PROBLEMA': 'bi-exclamation-triangle',
        'SOLUCION': 'bi-check-circle',
        'CALIDAD': 'bi-award',
        'FINAL': 'bi-flag-fill',
        'OTRO': 'bi-camera',
    }
    return iconos.get(tipo, 'bi-camera')