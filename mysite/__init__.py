from __future__ import absolute_import, unicode_literals

# 确保应用程序在 Django 启动时始终导入此应用程序
from .celery import app as celery_app

__all__ = ('celery_app',)
