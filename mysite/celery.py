from __future__ import absolute_import, unicode_literals

import logging
import os
from logging.handlers import RotatingFileHandler

from celery import Celery
from django.conf import settings

# 设置 Django 的默认设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')

# 使用 Django 的设置文件配置 Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动从所有已注册的 Django app 加载任务
app.autodiscover_tasks()

# 创建日志记录器
logger = logging.getLogger('celery')
logger.setLevel(logging.INFO)

# 创建处理程序
log_file_path = os.path.join(settings.BASE_DIR, 'logs/celery.log')
handler = RotatingFileHandler(log_file_path, maxBytes=10000, backupCount=3)

# 创建并设置格式化器
formatter = logging.Formatter('[%(asctime)s: %(levelname)s/%(processName)s] %(message)s')
handler.setFormatter(formatter)

# 添加处理程序到记录器
logger.addHandler(handler)