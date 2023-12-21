from django.core.management import call_command
from django.utils.autoreload import logger
from django_cron import CronJobBase, Schedule

from ims.models import Link


# 运行 Cron Job:
# python manage.py runcrons
# 通常，你会在服务器上设置一个定期运行 runcrons 命令的计划任务（例如，使用 crontab）。

class Runspider(CronJobBase):
    schedule = Schedule(run_at_times=['00:00'])
    code = 'ims.cron.Runspider'  # 一个唯一的代码

    def do(self):
        logger.info("CronJob:Runspider start ---------------------------------------")
        return
        call_command('runspider')


class VerifiedTelegram(CronJobBase):
    schedule = Schedule(run_every_mins=10)
    code = 'ims.cron.VerifiedTelegram'  # 一个唯一的代码

    def do(self):
        logger.info("CronJob:VerifiedTelegram start ---------------------------------------")
        call_command('verified_telegram')


class DeleteInvalidLinks(CronJobBase):
    schedule = Schedule(run_at_times=['13:00'])
    code = 'ims.cron.DeleteInvalidLinks'  # 一个唯一的代码

    def do(self):
        logger.info("CronJob:DeleteInvalidLinks start ---------------------------------------")
        Link.objects.verified_and_invalid().delete()
