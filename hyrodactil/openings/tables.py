
import django_tables2 as tables

from .models import Opening


class OpeningTable(tables.Table):
    title = tables.LinkColumn(
        'openings:detail_opening',
        args=[tables.A('pk')],
    )
    employment_type = tables.Column(verbose_name='Type')
    published_date = tables.DateColumn(verbose_name='Published', format='d/m/Y')
    location = tables.Column(
        accessor='get_location_string', order_by=('city', 'country')
    )
    number_applications = tables.LinkColumn(
        'applications:list_applications',
        args=[tables.A('pk')],
        verbose_name='Applications'
    )
    status = tables.Column(accessor='get_status')

    class Meta:
        attrs = {'class': 'large-12 columns'}
        model = Opening
        fields = (
            'title', 'employment_type', 'location',
            'number_applications', 'published_date', 'status'
        )
