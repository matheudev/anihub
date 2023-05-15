from django import template
from datetime import datetime

register = template.Library()

@register.simple_tag
def year_range(start_year):
    current_year = datetime.now().year
    return reversed(range(start_year, current_year + 2))
