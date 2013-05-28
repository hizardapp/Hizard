from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

import django_tables2 as tables

from .models import Opening


class OpeningTable(tables.Table):
    title = tables.LinkColumn(
        'openings:detail_opening',
        args=[tables.A('pk')],
    )
    department = tables.Column()
    employment_type = tables.Column(verbose_name=_('Type'))
    published_date = tables.DateColumn(
        verbose_name=_('Published'), format='d/m/Y'
    )
    location = tables.Column(
        accessor='get_location_string', order_by=('city', 'country')
    )
    number_applications = tables.Column(
        verbose_name=_('Applications')
    )
    status = tables.Column(accessor='get_status')

    def render_number_applications(self, record):
        get_param = '?openings=%s' % record.pk
        return mark_safe("<a href=\"%s\">%s</a>" % (
            reverse('applications:list_applications') + get_param,
            record.number_applications
        ))

    class Meta:
        attrs = {'class': 'large-12 columns'}
        model = Opening
        fields = (
            'title', 'department', 'employment_type', 'location',
            'number_applications', 'published_date', 'status'
        )
