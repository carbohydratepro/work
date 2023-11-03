from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    original_string, replacement_string = arg.split(',')
    return value.replace(original_string, replacement_string)
