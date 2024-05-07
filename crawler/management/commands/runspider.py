import logging
import random
import time

from django.core.management.base import BaseCommand

import common.utils
from crawler.spiders.spider import scrape_with_xpath
from crawler.tgcng_com import get_telegram_url, get_words, get_info_ids, get_words_by_db
from ims.models import Link
from ims.services import get_or_create_link

from crawler.tgcng_com import Run

logger = logging.getLogger('django')

class Command(BaseCommand):
    help = 'Run the web scraper'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # 记录开始时间和允许的最大运行时间
    #     self.start_time = time.time()
    #     self.max_minutes = 1

    # # 是否超时
    # def is_timeout(self):
    #     return time.time() - self.start_time > self.max_minutes * 60

    # def check_timeout(self):
    #     if self.is_timeout():
    #         logger.info("Command: runspider timeout -----------------")
    #         return True
    #     return False

    # def random_sleep(self, num_a, num_b):
    #     time.sleep(random.uniform(num_a, num_b))

    def handle(self, *args, **kwargs):
        logger.info("Command: runspider start -----------------")
        # return

        Run().handle()

        

        # num_a = 0.2
        # num_b = 1.0
        # # for word in get_words():
        # # urls = [
        # #     'https://www.tgcng.com/tags.php',
        # #     'https://github.com/itgoyo/TelegramGroup',
        # #     'https://github.com/jackhawks/rectg',
        # #     'https://s.weibo.com/top/summary',
        # # ]
        # # url = random.choice(urls)
        # # words = get_words(url=url)
        # words = get_words_by_db()
        # for word in words[:100]:

        #     if self.check_timeout():
        #         return

        #     ids = get_info_ids(word)
        #     for info_id in ids[:100]:

        #         if self.check_timeout():
        #             return

        #         telegram_url = get_telegram_url(info_id)
        #         if telegram_url:
        #             get_or_create_link(url=telegram_url)

        #         self.random_sleep(num_a, num_b)
        #     self.random_sleep(num_a, num_b)
    
