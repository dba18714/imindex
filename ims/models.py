import logging
import pprint
import re
import uuid

import requests
from bs4 import BeautifulSoup
from django.db import models
from django.utils.timezone import now

from ims import tasks

from django.utils.autoreload import logger


class Link(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    member_count = models.IntegerField(default=0)
    url = models.URLField(unique=True)  # Telegram链接
    is_valid = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # 调用父类的 save 方法
        tasks.verified_telegram.delay(self.id)
        logger.error(f"------ call tasks.verified_telegram.delay")

    def verified_telegram(self):
        try:
            url = self.url
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'lxml')

                # 提取 Telegram 名称和描述
                telegram_name = soup.select_one('.tgme_page_title span')
                self.name = telegram_name.text if telegram_name else 'none'

                telegram_description = soup.select_one('.tgme_page_description')
                self.description = telegram_description.text if telegram_description else 'none'

                telegram_member_count = soup.select_one('.tgme_page_extra')
                if telegram_member_count:
                    member_count = telegram_member_count.text
                    member_count = re.findall(r'\d+', member_count)
                    member_count = ''.join(member_count)
                    self.member_count = member_count if member_count else 0

                # 检查是否有效
                self.is_valid = True
                robots_meta = soup.find('meta', attrs={'name': 'robots'})
                if robots_meta and robots_meta.get('content') != 'none':
                    self.is_valid = False

                self.verified_at = now()
                self.save()

            else:
                # 记录错误日志
                logger.error("HTTP 请求失败" + pprint.pformat({
                    'URL': url,
                    'status': response.status_code,
                    'headers': response.headers,
                    'body': response.text,
                }, indent=4))

        except Exception as e:
            logger.error(f"发生异常: {e}")
