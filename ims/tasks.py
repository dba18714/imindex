import random
import time

from celery import shared_task
from django.apps import apps
from django.utils.autoreload import logger

from crawler.tgcng_com import get_words, get_info_ids, get_telegram_url
# from ims.models import Link
Link = apps.get_model('ims', 'Link')

@shared_task
def verified_telegram(link_id):
    logger.error(f"verified_telegram start")
    from ims.models import Link
    # time.sleep(10)
    link = Link.objects.get(id=link_id)
    link.verified_telegram()
    logger.error(f"verified_telegram Done")
    return 'Done'


@shared_task
def spider_for_tgcng_com():
    num_a = 1.0
    num_b = 20.0
    for word in get_words():
        ids = get_info_ids(word)
        for info_id in ids:
            url = get_telegram_url(info_id)
            if url:
                link, created = Link.objects.get_or_create(url=url)
            time.sleep(random.uniform(num_a, num_b))

