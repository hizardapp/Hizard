from django import template

register = template.Library()


@register.filter
def inside(key, container):
    return key in container


@register.filter
def lookup(container, key):
    return container[key]
