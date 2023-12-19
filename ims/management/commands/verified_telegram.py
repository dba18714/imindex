import random
import time

from django.core.management.base import BaseCommand

import common.utils
from crawler.spiders.spider import save_data_to_model, scrape_with_xpath
from ims.models import Link
from ims import tasks


class Command(BaseCommand):
    help = 'verified_telegram.py'

    def handle(self, *args, **kwargs):
        link = Link.objects.order_by('verified_at', 'created_at').first()
        if link:
            tasks.verified_telegram.delay(link.id)
