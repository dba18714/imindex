import random
import time

from django.core.management.base import BaseCommand

import common.utils
from crawler.spiders.spider import scrape_with_xpath
from crawler.tgcng_com import get_telegram_url, get_words, get_info_ids
from ims.models import Link


class Command(BaseCommand):
    help = 'Run the web scraper'

    # def handle(self, *args, **kwargs):
    #     num_a = 1.0
    #     num_b = 20.0
    #     for word in get_words():
    #         ids = get_info_ids(word)
    #         for info_id in ids:
    #             url = get_telegram_url(info_id)
    #             if url:
    #                 link, created = Link.objects.get_or_create(url=url)
    #             time.sleep(random.uniform(num_a, num_b))
    #
