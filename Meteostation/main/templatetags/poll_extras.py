# from django import template
from django.template.defaulttags import register
import re


# register = template.library()

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)


@register.filter
def modify(dictionary, string):
    newstr = string
    for key in dictionary:
        newstr = newstr.replace(key, dictionary[key])
    return newstr


# @register.filter
# def get_name(value):
#     return value.__name__


@register.simple_tag
def replace(string, regex, replacement):
    return re.sub(regex, replacement, string)
