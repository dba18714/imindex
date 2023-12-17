from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = '描述你的命令做什么'

    def add_arguments(self, parser):
        # 添加命令行参数
        pass

    def handle(self, *args, **kwargs):
        # 命令的主要逻辑写在这里

        # 创建管理员
        username = "admin"
        password = "Admin123"
        email = "admin@admin.com"
        if User.objects.exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'管理员 "{username}" 已创建'))
