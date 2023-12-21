import logging
import pprint
import re
import uuid

import requests
from bs4 import BeautifulSoup
from django.contrib import admin
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from ims import tasks

from django.utils.autoreload import logger


class LinkManager(models.Manager):
    def verified_and_invalid(self):
        return self.filter(verified_at__isnull=False, is_valid=False)

    def verified_and_valid(self):
        return self.filter(verified_at__isnull=False, is_valid=True)


class Search(models.Model):
    keyword = models.CharField(max_length=255, unique=True)
    search_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_search_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.keyword


class Link(models.Model):
    UNKNOWN = 'unknown'
    GROUP = 'group'
    CHANNEL = 'channel'
    PERSONAL = 'personal'

    CATEGORY_CHOICES = [
        (UNKNOWN, _('Unknown')),
        (GROUP, _('Group')),
        (CHANNEL, _('Channel')),
        (PERSONAL, _('Personal')),
    ]

    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default=UNKNOWN)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(default="Updating...", max_length=128, verbose_name=_("Name"))
    description = models.CharField(max_length=512, verbose_name=_("Description"))
    member_count = models.IntegerField(default=0)
    url = models.URLField(unique=True)  # Telegram链接
    is_valid = models.BooleanField(default=False, verbose_name=_("有效的"))
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = LinkManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # 检查是否是新创建的对象
        if self.pk is None:
            url_changed = True
        else:
            # 获取当前数据库中的对象
            old_object = Link.objects.get(pk=self.pk)
            # 检查 'url' 字段是否改变
            url_changed = old_object.url != self.url

        # 调用父类的 save 方法保存对象
        super().save(*args, **kwargs)

        # 如果 'url' 发生了变化，则执行操作
        if url_changed:
            tasks.verified_telegram.delay(self.id)
            logger.error("------ call tasks.verified_telegram.delay")

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
                    match = re.search(r'(\d[\d\s,]*)members', telegram_member_count.text)
                    if match:
                        self.member_count = int(re.sub(r'\D', '', match.group(1)))
                        self.category = self.GROUP
                    match = re.search(r'(\d[\d\s,]*)subscribers', telegram_member_count.text)
                    if match:
                        self.member_count = int(re.sub(r'\D', '', match.group(1)))
                        self.category = self.CHANNEL
                    match = re.search(r'^@\w+$', telegram_member_count.text)
                    if match:
                        self.category = self.PERSONAL

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
