import time
import logging

from constance import config
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django_unicorn.components import UnicornView
from django.core.paginator import Paginator

from .. import tasks
from ..models import Link
from ..services import get_or_create_link

# from django.utils.autoreload import logger

logger = logging.getLogger('django')


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)
        return True
    except ValidationError:
        return False


class AddView(UnicornView):

    url = ""
    links = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # time.sleep(3)

    def add(self):
        # print(config.MY_SETTING)
        print(settings.ALLOWED_HOSTS)
        # logger.error(f"zzzzzzxxxxxxx------")
        self.links = []
        url = self.url

        if not url:
            messages.error(self.request, "链接不能为空！")
            return

        # 分割字符串为行
        lines = url.splitlines()

        # 遍历每一行
        for url in lines:
            url = url.strip()
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            if not is_valid_url(url):
                messages.error(self.request, "链接格式无效：" + url)
                continue

            link, created = get_or_create_link(url=url)
            if not created:
                tasks.verify_telegram.delay(link.id)
            self.links.append(link)
            messages.success(self.request, "添加成功")
