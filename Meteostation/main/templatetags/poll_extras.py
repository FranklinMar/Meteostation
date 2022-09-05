# from django import template
from django.template.defaulttags import register


# register = template.library()

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)


# @register.filter
# def replace(value, arg):
#     """
#     Replacing filter
#     Use `{{ "aaa"|replace:"a|b" }}`
#     """
#     if len(arg.split('|')) != 2:
#         return value
#
#     what, to = arg.split('|')
#     return value.replace(what, to)

@register.filter
def modify(dictionary, string):
    newstr = string
    for key in dictionary:
        newstr = newstr.replace(key, dictionary[key])
    return newstr
