from django import template

register = template.Library()

@register.filter
def get_status_count(animelist, status):
    return animelist.filter(status=status).count()
