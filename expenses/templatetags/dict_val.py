from django import template
register = template.Library()

@register.filter
def dict_val(dict_var, key):
    return dict_var[key]