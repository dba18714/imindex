import time
import logging

logger = logging.getLogger(__name__)

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django_unicorn.components import UnicornView
from django.core.paginator import Paginator
from ..models import Link


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

    def add(self):
        self.links = []
        url = self.url

        if not url:
            messages.error(self.request, "链接不能为空")
            return

        # 分割字符串为行
        lines = url.splitlines()

        # 遍历每一行
        for url in lines:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            if not is_valid_url(url):
                messages.error(self.request, "链接格式无效：" + url)
                continue

            link, created = Link.objects.get_or_create(url=url)
            link.save()
            self.links.append(link)
            messages.success(self.request, "添加成功")