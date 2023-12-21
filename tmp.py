import os
import django
from django.db.models import F

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# 初始化 Django
django.setup()

from ims.models import Link

links = Link.objects.order_by(F('verified_at').asc(nulls_first=True), 'created_at')[:2000]

for link in links:
    print(link.verified_at)
