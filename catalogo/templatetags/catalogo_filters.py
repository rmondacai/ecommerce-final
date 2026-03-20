from django import template

register = template.Library()


@register.filter(name='formato_clp')
def formato_clp(value):
    """Formatea un número como moneda chilena. Ej: 15990 -> $15.990"""
    try:
        value = int(value)
        return f"${value:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return value
