from django import template

register = template.Library()

@register.simple_tag
def get_dict_value_by_key(dictionary, key,*args, **kwargs):
    "Call dictionary by given key"
    return dictionary.get(key)

@register.simple_tag
def get_sum_of_values(*args):
    "Sum values of given args"
    return sum(args)

