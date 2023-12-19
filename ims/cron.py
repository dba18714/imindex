from django.core.management import call_command
from django.utils.autoreload import logger
from django_cron import CronJobBase, Schedule

from ims.models import Link


# 运行 Cron Job:
# python manage.py runcrons
# 通常，你会在服务器上设置一个定期运行 runcrons 命令的计划任务（例如，使用 crontab）。

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # 每N分钟运行一次

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'ims.cron.MyCronJob'  # 一个唯一的代码

    def do(self):
        # logger.error("MyCronJob start ---------------------------------------")
        # return "MyCronJob Done"
        call_command('runspider')


class VerifiedTelegram(CronJobBase):
    RUN_EVERY_MINS = 10  # 每N分钟运行一次

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'ims.cron.VerifiedTelegram'  # 一个唯一的代码

    def do(self):
        # logger.error("MyCronJob start ---------------------------------------")
        # return "MyCronJob Done"
        call_command('verified_telegram')


class DeleteInvalidLinks(CronJobBase):
    schedule = Schedule(run_at_times=['13:00'])  # 数字 0 到 6 分别代表星期天到星期六
    code = 'ims.cron.DeleteInvalidLinks'  # 一个唯一的代码

    def do(self):
        # logger.error("MyCronJob start ---------------------------------------")
        # return "MyCronJob Done"
        Link.objects.verified_and_invalid().delete()
