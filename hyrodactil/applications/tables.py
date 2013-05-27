from django.utils.translation import ugettext_lazy as _

import django_tables2 as tables

from .models import Application


class ApplicationTable(tables.Table):
    first_name = tables.Column(accessor="applicant.first_name")
    last_name = tables.Column(accessor="applicant.last_name")
    created = tables.DateColumn(verbose_name=_("Date applied"), format="d/m/Y H:m")
    status = tables.Column(accessor="current_stage")

    class Meta:
        attrs = {"class": "large-12 columns"}
        model = Application
        fields = ("first_name", "last_name", "created")

class AllApplicationsTable(ApplicationTable):
    opening = tables.LinkColumn("openings:detail_opening",
            args=[tables.A("opening.pk")],
            verbose_name=_("Opening"),
            accessor="opening.title")
