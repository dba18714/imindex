from django.core.management.base import BaseCommand
from django.db.models import F

from ims import tasks
from ims.models import Link


def get_first_link():
    return Link.objects.order_by(F('verified_at').asc(nulls_first=True), 'created_at').first()


class Command(BaseCommand):
    help = 'verified_telegram.py'

    def handle(self, *args, **kwargs):
        link = get_first_link()
        if link:
            tasks.verified_telegram.delay(link.id)
