from django.core.management.base import NoArgsCommand
from core.utils import delete_demo_company, create_demo_account


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        delete_demo_company()
        create_demo_account()
