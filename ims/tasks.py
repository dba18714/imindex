import random
import time

from celery import shared_task
from django.apps import apps
# from django.utils.autoreload import logger

from crawler.tgcng_com import get_words, get_info_ids, get_telegram_url
from crawler.tgsou_me import get_telegram_urls
from ims import services


@shared_task
def verify_telegram(link_id):
    services.verify_telegram(link_id)


@shared_task
def spider_for_tgcng_com():
    from ims.models import Link
    num_a = 1.0
    num_b = 10.0
    # for word in get_words():
    ids = get_info_ids(get_words()[0])
    for info_id in ids[:20]:
        telegram_url = get_telegram_url(info_id)
        if telegram_url:
            link, created = Link.objects.get_or_create(url=telegram_url)
        time.sleep(random.uniform(num_a, num_b))


@shared_task
def spider_for_tgsou_me():
    from ims.models import Link
    num_a = 1.0
    num_b = 10.0
    telegram_urls = get_telegram_urls()[:20]
    for telegram_url in telegram_urls:
        if telegram_url:
            link, created = Link.objects.get_or_create(url=telegram_url)
            time.sleep(random.uniform(num_a, num_b))

