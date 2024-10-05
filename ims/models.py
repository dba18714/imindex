import logging
import pprint
import re
import uuid

import requests
from bs4 import BeautifulSoup
from django.contrib import admin
from django.db import models, transaction
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from ims import tasks

# from django.utils.autoreload import logger


class LinkManager(models.Manager):
    def verified_and_invalid(self):
        return self.filter(verified_at__isnull=False, is_valid=False)

    def verified_and_valid(self):
        return self.filter(verified_at__isnull=False, is_valid=True)


class Search(models.Model):
    keyword = models.CharField(max_length=255, unique=True)
    search_count = models.IntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_search_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.keyword


class Ad(models.Model):

    PLACE_CHOICES = [
        (1, _('首页')),
        (2, _('详情页')),
    ]

    title = models.CharField(max_length=255, unique=True)
    place = models.SmallIntegerField(choices=PLACE_CHOICES)
    url = models.CharField(null=True, blank=True)
    image = models.ImageField(upload_to='', null=True, blank=True)
    click_count = models.IntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    def __str__(self):
        return self.title


class Link(models.Model):
    UNKNOWN = 'unknown'
    GROUP = 'group'
    CHANNEL = 'channel'
    PERSONAL = 'personal'

    CATEGORY_CHOICES = [
        (UNKNOWN, _('未知')),
        (GROUP, _('群组')),
        (CHANNEL, _('频道')),
        (PERSONAL, _('个人')),
    ]

    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default=UNKNOWN)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(default="Updating...", max_length=128, verbose_name=_("Name"))
    description = models.CharField(max_length=512, verbose_name=_("Description"))
    member_count = models.IntegerField(default=0, verbose_name=_("用户数"))
    url = models.URLField(unique=True)  # Telegram链接
    
    # true则是用户提交的链接，false则是爬虫爬取的链接
    is_by_user = models.BooleanField(default=False, verbose_name=_("是否是用户提交的链接"))

    is_valid = models.BooleanField(default=False, verbose_name=_("有效的"))
    verified_at = models.DateTimeField(null=True, blank=True, verbose_name=_("验证时间"))

    #验证开始时间，不管是否验证成功
    verified_start_at = models.DateTimeField(null=True, blank=True, verbose_name=_("验证开始时间"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("创建时间"))
    updated_at = models.DateTimeField(auto_now=True)

    objects = LinkManager()

    def get_absolute_url(self):
        return reverse('ims:detail', args=[str(self.uuid)])

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
            # tasks.verify_telegram.delay(self.id)
            # 确保在事务提交后执行任务
            transaction.on_commit(lambda: tasks.verify_telegram_dispatch(self.id))

    # def verified_telegram(self):
        # try:
        #     url = self.url
        #     headers = {
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        #     }
        #     response = requests.get(url, headers=headers)
        #
        #     if response.status_code == 200:
        #         html = response.text
        #         soup = BeautifulSoup(html, 'lxml')
        #
        #         # 提取 Telegram 名称和描述
        #         telegram_name = soup.select_one('.tgme_page_title span')
        #         self.name = telegram_name.text if telegram_name else 'none'
        #
        #         telegram_description = soup.select_one('.tgme_page_description')
        #         self.description = telegram_description.text if telegram_description else 'none'
        #
        #         telegram_member_count = soup.select_one('.tgme_page_extra')
        #         if telegram_member_count:
        #             match = re.search(r'(\d[\d\s,]*)members', telegram_member_count.text)
        #             if match:
        #                 self.member_count = int(re.sub(r'\D', '', match.group(1)))
        #                 self.category = self.GROUP
        #             match = re.search(r'(\d[\d\s,]*)subscribers', telegram_member_count.text)
        #             if match:
        #                 self.member_count = int(re.sub(r'\D', '', match.group(1)))
        #                 self.category = self.CHANNEL
        #             match = re.search(r'^@\w+$', telegram_member_count.text)
        #             if match:
        #                 self.category = self.PERSONAL
        #
        #         # 检查是否有效
        #         self.is_valid = True
        #         robots_meta = soup.find('meta', attrs={'name': 'robots'})
        #         if robots_meta and robots_meta.get('content') != 'none':
        #             self.is_valid = False
        #
        #         self.verified_at = now()
        #         self.save()
        #
        #     else:
        #         # 记录错误日志
        #         logger.error("HTTP 请求失败" + pprint.pformat({
        #             'URL': url,
        #             'status': response.status_code,
        #             'headers': response.headers,
        #             'body': response.text,
        #         }, indent=4))
        #
        # except Exception as e:
        #     logger.error(f"发生异常: {e}")
