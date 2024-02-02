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
from ims.services import get_or_create_link

logger = logging.getLogger('django')


@shared_task
def verify_telegram(link_id):
    logger.info("task verify_telegram start -----------------")
    services.verify_telegram(link_id)


@shared_task
def spider_for_tgcng_com():
    logger.info("spider_for_tgcng_com start -----------------")
    num_a = 1.0
    num_b = 2.0
    # for word in get_words():
    urls = [
        'https://www.tgcng.com/tags.php',
        'https://github.com/itgoyo/TelegramGroup',
        'https://github.com/jackhawks/rectg',
        'https://s.weibo.com/top/summary',
    ]
    url = random.choice(urls)
    ids = get_info_ids(get_words(url=url)[0])
    for info_id in ids[:50]:
        telegram_url = get_telegram_url(info_id)
        if telegram_url:
            get_or_create_link(url=telegram_url)
            time.sleep(random.uniform(num_a, num_b))


@shared_task
def spider_for_tgsou_me():
    exit()
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
    exit()
    logger.info("spider_for_tgsou_me_from_html start -----------------")
    num_a = 1.0
    num_b = 10.0
    telegram_urls = get_telegram_urls_of_html()[:20]
    logger.info(f"telegram_urls: {telegram_urls}")
    for telegram_url in telegram_urls:
        if telegram_url:
            get_or_create_link(url=telegram_url)
            time.sleep(random.uniform(num_a, num_b))
