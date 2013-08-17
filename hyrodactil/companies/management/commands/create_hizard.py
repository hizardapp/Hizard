import datetime

from django.core.management.base import NoArgsCommand

from ...models import Company
from core.utils import setup_company


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        hizard = Company.objects.create(name="Hizard",
            subdomain="hizard",
            website="http://hizard.com",
            description="")
        setup_company(hizard)
        hizard.opening_set.all().update(published_date=datetime.datetime.now())

