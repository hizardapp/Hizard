import logging

from django import template
from django.core.urlresolvers import resolve

register = template.Library()
logger = logging.getLogger(__name__)


class ActiveUrlNode(template.Node):
    def __init__(self, request, names, return_value='active-link'):
        self.request = template.Variable(request)
        self.names = [template.Variable(n) for n in names]
        self.return_value = template.Variable(return_value)

    def render(self, context):
        request = self.request.resolve(context)
        any_of = False
        try:
            url = resolve(request.path_info)
            url_name = "%s:%s" % (url.namespace, url.url_name)
            for n in self.names:
                name = n.resolve(context)
                if url_name.startswith(name):
                    any_of = True
                    break
        except:
            return ''

        return self.return_value if any_of else ''


@register.tag
def active(parser, token):
    """
        Simple tag to check which page we are on, based on resolve;
        Useful to add an 'active' css class in menu items that needs to be
        aware when they are selected.

        Usage:

            {% active request "base:index" %}
            {% active request "base:index" "base:my_view" %}
    """
    try:
        args = token.split_contents()
        return ActiveUrlNode(args[1], args[2:])
    except IndexError:
        raise template.TemplateSyntaxError, "%r tag requires at least 2 arguments" % token.contents.split()[0]
