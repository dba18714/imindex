from django.core.management import call_command
from django.utils.autoreload import logger
from django_cron import CronJobBase, Schedule


# 运行 Cron Job:
# python manage.py runcrons
# 通常，你会在服务器上设置一个定期运行 runcrons 命令的计划任务（例如，使用 crontab）。

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # 每N分钟运行一次

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'ims.my_cron_job'  # 一个唯一的代码

    def do(self):
        logger.error("MyCronJob start ---------------------------------------")
        return "MyCronJob Done"
        call_command('runspider')
