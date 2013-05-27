import django_tables2 as tables

from .models import Application


class ApplicationTable(tables.Table):
    first_name = tables.Column(accessor="applicant.first_name")
    last_name = tables.Column(accessor="applicant.last_name")
    created = tables.DateColumn(verbose_name="Date applied", format="d/m/Y H:m")
    status = tables.Column(accessor="current_stage")

    class Meta:
        attrs = {"class": "large-12 columns"}
        model = Application
        fields = ("first_name", "last_name", "created")

class AllApplicationsTable(ApplicationTable):
    opening = tables.Column(verbose_name="Opening", accessor="opening.title")
