from django.utils.translation import ugettext_lazy as _

import django_tables2 as tables

from .models import Application


class ApplicationsTable(tables.Table):
    name = tables.LinkColumn(
        'applications:application_detail',
        args=[tables.A('pk')],
        accessor='applicant.get_full_name',
        order_by=('applicant.first_name', 'applicant.last_name')
    )
    created = tables.DateColumn(verbose_name=_("Date applied"), format="d/m/Y")
    status = tables.Column(accessor="current_stage")
    opening = tables.LinkColumn(
        "openings:detail_opening",
        args=[tables.A("opening.pk")],
        verbose_name=_("Opening"),
        accessor="opening.title"
    )

    class Meta:
        attrs = {"class": "large-12 columns"}
        model = Application
        fields = ('name', "created")
