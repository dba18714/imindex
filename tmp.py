import os
import random

import django
from django.db.models import F

from ims.tasks import get_or_create_link

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# 初始化 Django
django.setup()

from ims.models import Link

link, created = get_or_create_link('https://tnav.me/22')
print(link.id, created)
exit()

links = Link.objects.order_by(F('verified_at').asc(nulls_first=True), 'created_at')[:3]

for link in links:
    print(link.id)

links_list = list(links)
print(links_list)

# 对列表进行随机排序
random.shuffle(links_list)

# 打印随机排序后的顺序
for link in links_list:
    print(link.id)
