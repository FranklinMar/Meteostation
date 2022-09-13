# from django import template
from django.template.defaulttags import register


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
