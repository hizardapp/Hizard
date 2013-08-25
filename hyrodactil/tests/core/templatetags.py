from django_webtest import WebTest

from django import template


class Tests(WebTest):
    def test_active_syntax(self):
        with self.assertRaises(template.TemplateSyntaxError):
            template.Template("""{% load core_extra %}{% active %}""")

