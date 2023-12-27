import logging
import random
import time

from celery import shared_task
from django.apps import apps
from django.db.models import Q
from django.forms import model_to_dict

# from django.utils.autoreload import logger

from crawler.tgcng_com import get_words, get_info_ids, get_telegram_url
from crawler.tgsou_me import get_telegram_urls_of_xml, get_telegram_urls_of_html
from ims import services

logger = logging.getLogger('django')


def get_or_create_link(url):
    from ims.models import Link
    link, created = Link.objects.get_or_create(
        Q(url__iexact=url),
        defaults={'url': url}  # 如果需要创建新对象，则使用这些默认值
    )
    return link, created


@shared_task
def verify_telegram(link_id):
    logger.info("task verify_telegram start -----------------")
    services.verify_telegram(link_id)


@shared_task
def spider_for_tgcng_com():
    logger.info("spider_for_tgcng_com start -----------------")
    num_a = 1.0
    num_b = 10.0
    # for word in get_words():
    ids = get_info_ids(get_words()[0])
    for info_id in ids[:50]:
        telegram_url = get_telegram_url(info_id)
        if telegram_url:
            get_or_create_link(url=telegram_url)
        time.sleep(random.uniform(num_a, num_b))


@shared_task
def spider_for_tgsou_me():
    logger.info("spider_for_tgsou_me start -----------------")
    num_a = 1.0
    num_b = 10.0
    telegram_urls = get_telegram_urls_of_xml()[:20]
    logger.info(f"telegram_urls: {telegram_urls}")
    for telegram_url in telegram_urls:
        if telegram_url:
            get_or_create_link(url=telegram_url)
            time.sleep(random.uniform(num_a, num_b))


@shared_task
def spider_for_tgsou_me_from_html():
    logger.info("spider_for_tgsou_me_from_html start -----------------")
    num_a = 1.0
    num_b = 10.0
    telegram_urls = get_telegram_urls_of_html()[:20]
    logger.info(f"telegram_urls: {telegram_urls}")
    for telegram_url in telegram_urls:
        if telegram_url:
            get_or_create_link(url=telegram_url)
            time.sleep(random.uniform(num_a, num_b))
