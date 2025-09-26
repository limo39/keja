from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter"""
    if value:
        return [item.strip() for item in value.split(delimiter) if item.strip()]
    return []

@register.filter
def strip(value):
    """Strip whitespace from a string"""
    if value:
        return value.strip()
    return value