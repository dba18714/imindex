import random
import time

from django.core.management.base import BaseCommand

import common.utils
from crawler.spiders.spider import save_data_to_model, scrape_with_xpath


class Command(BaseCommand):
    help = 'Run the web scraper'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('is running runspider.py'))
        for i in range(10):
            random_integer = random.randint(2000, 3762832)
            url = f"https://www.tgcng.com/info.php?gid={random_integer}"
            xpath = '/html/body/div[@id="__nuxt"]/div[@id="__layout"]/div[@id="app"]/div[@class="container"]/div[@class="info"]/a[@class="item"]/div[@class="member"]'

            text_contents = scrape_with_xpath(url, xpath)
            url = common.utils.extract_url_of_str(text_contents[0])
            link, created = save_data_to_model(url)  # 保存数据到数据库
            if created:
                self.stdout.write(self.style.SUCCESS('Successfully scraped website:'))
                self.stdout.write(self.style.SUCCESS(link.url + ' Created: ' + str(created)))

            random_float = random.uniform(1.0, 3.0)
            self.stdout.write(self.style.WARNING(str(random_integer) + "|" + str(random_float)))
            time.sleep(random_float)
