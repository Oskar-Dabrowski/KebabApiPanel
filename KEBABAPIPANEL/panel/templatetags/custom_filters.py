import json
from django import template

register = template.Library()

@register.filter
def parse_json(value):
    """Parsuje string JSON na słownik."""
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return {}
