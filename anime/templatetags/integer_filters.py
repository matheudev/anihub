from django import template

register = template.Library()

@register.filter
def as_integer(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return value
