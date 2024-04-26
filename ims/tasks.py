import logging
import random
import time

from celery import shared_task
from django.apps import apps
from django.db.models import Q
from django.forms import model_to_dict
import redis

# from django.utils.autoreload import logger

from crawler.tgcng_com import get_words, get_info_ids, get_telegram_url, get_words_by_db
from crawler.tgsou_me import get_telegram_urls_of_xml, get_telegram_urls_of_html
from ims import services
from ims.services import get_or_create_link
from django.utils.timezone import now

logger = logging.getLogger('django')


# @shared_task
@shared_task(priority=10)
def verify_telegram(link_id):
    logger.info(f"task verify_telegram start link_id: {link_id} -----------------")

    # from ims.models import Link
    # link = Link.objects.get(id=link_id)
    # link.verified_start_at = now()
    # link.save()


    # 创建一个Redis连接
    r = redis.Redis(host='redis', port=6379, db=0, password='RDFGDxpI1h')

    # 创建一个锁
    lock = r.lock('verify_telegram')

    # 获取锁
    lock.acquire(blocking=True)

    try:
        # 在这里执行你的代码
        services.verify_telegram(link_id)
        time.sleep(10)
    finally:
        # 无论是否发生错误，都要释放锁
        lock.release()



def verify_telegram_dispatch(link_id):
    from ims.models import Link
    link = Link.objects.get(id=link_id)
    link.verified_start_at = now()
    link.save()

    verify_telegram.delay(link_id)


@shared_task
def spider_for_tgcng_com():
    logger.info("spider_for_tgcng_com start -----------------")
    num_a = 0.2
    num_b = 1.0
    # for word in get_words():
    # urls = [
    #     'https://www.tgcng.com/tags.php',
    #     'https://github.com/itgoyo/TelegramGroup',
    #     'https://github.com/jackhawks/rectg',
    #     'https://s.weibo.com/top/summary',
    # ]
    # url = random.choice(urls)
    # words = get_words(url=url)
    words = get_words_by_db()
    for word in words[:10]:
        ids = get_info_ids(word)
        for info_id in ids[:14]:
            telegram_url = get_telegram_url(info_id)
            if telegram_url:
                get_or_create_link(url=telegram_url)
                time.sleep(random.uniform(num_a, num_b))
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
