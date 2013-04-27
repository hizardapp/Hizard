from django import template

register = template.Library()


@register.filter(is_safe=False)
def concatenate(value, arg):
    """Merge string."""
    try:
        return str(value) + str(arg)
    except (TypeError):
        return ''