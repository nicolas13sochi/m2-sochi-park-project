from django import template

register = template.Library()

@register.simple_tag
def call_obj_method(obj, method_name, *args, **kwargs):
    "Call obj's method and pass it the given parameters"
    return getattr(obj, method_name)(*args, **kwargs)
