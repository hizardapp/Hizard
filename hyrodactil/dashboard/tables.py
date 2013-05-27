from django.utils.translation import ugettext_lazy as _

import django_tables2 as tables

from openings.models import Opening


class OpeningTable(tables.Table):
    title = tables.LinkColumn(
        'openings:detail_opening',
        args=[tables.A('pk')],
    )

    class Meta:
      model = Opening
      fields = ("title",)
