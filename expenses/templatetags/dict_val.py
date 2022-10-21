from django import template
register = template.Library()

@register.filter
def dict_val(dict_var, key):
    try:
        return dict_var[key]

    except KeyError:
        return 0