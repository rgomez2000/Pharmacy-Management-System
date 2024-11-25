from django import template

register = template.Library()

@register.filter
def get(value, idx):
    # Returns the entry located at index `idx` of iterable `value`
    return value[idx]

@register.filter
def to_list(value):
    return list(value)