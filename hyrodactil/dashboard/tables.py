import django_tables2 as tables

from openings.models import Opening
from companysettings.models import InterviewStage


class OpeningTable(tables.Table):
    title = tables.LinkColumn(
        'openings:detail_opening',
        args=[tables.A('pk')],
    )

    def __init__(self, company, *args, **kwargs):
        for stage in InterviewStage.objects.filter(company=company):
            self.base_columns[str(stage.name)] = tables.Column(
                orderable=False,
                verbose_name=stage.name,
                accessor=tables.A("count_applications-%s" % stage.pk))
        super(OpeningTable, self).__init__(*args, **kwargs)

    class Meta:
      model = Opening
      fields = ("title",)
