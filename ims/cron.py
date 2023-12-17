from django.core.management import call_command
from django_cron import CronJobBase, Schedule


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # 每N分钟运行一次

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'ims.my_cron_job'  # 一个唯一的代码

    def do(self):
        print("---------------------------------------")
        call_command('runspider')
