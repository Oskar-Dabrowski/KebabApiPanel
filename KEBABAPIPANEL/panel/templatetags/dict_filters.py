
from django import template

register = template.Library()

@register.filter
def dict_get(dictionary, key):
    """
    Pobiera wartość z słownika dla podanego klucza.
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key, {})
    return {}