
import django_tables2 as tables

from .models import Opening


class OpeningTable(tables.Table):
    title = tables.Column()
    employment_type = tables.Column(verbose_name='Type')
    created = tables.DateColumn(verbose_name='Created', format='d/m/Y')
    location = tables.Column(
        accessor='get_location_string', order_by=('loc_city', 'loc_country')
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
            'number_applications', 'created', 'status'
        )
