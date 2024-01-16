import logging

from django.core.management import call_command
from django.db.models import F
from django.forms import model_to_dict
from django.utils.formats import date_format
# from django.utils.autoreload import logger
from django_cron import CronJobBase, Schedule

from ims import tasks
from ims.models import Link

logger = logging.getLogger('django')


# 运行 Cron Job:
# python manage.py runcrons
# 通常，你会在服务器上设置一个定期运行 runcrons 命令的计划任务（例如，使用 crontab）。

class Runspider(CronJobBase):
    schedule = Schedule(run_every_mins=1)
    code = 'ims.cron.Runspider'  # 一个唯一的代码
    allow_parallel_runs = False  # 防止任务重叠，如果上一个任务实例仍在运行，新的实例将不会启动

    def do(self):
        logger.info("CronJob:Runspider start -----------------")
        # call_command('runspider')
        tasks.spider_for_tgcng_com.delay()
        # tasks.spider_for_tgsou_me_from_html.delay()  # 已被cf拦截请求
        # tasks.spider_for_tgsou_me.delay()  # 已被cf拦截请求


def get_first_link():
    return Link.objects.order_by(F('verified_at').asc(nulls_first=True), 'created_at').first()


class VerifyTelegram(CronJobBase):
    schedule = Schedule(run_every_mins=1)
    code = 'ims.cron.VerifyTelegram'  # 一个唯一的代码
    allow_parallel_runs = False  # 防止任务重叠，如果上一个任务实例仍在运行，新的实例将不会启动

    def do(self):
        logger.info("CronJob:VerifyTelegram start -----------------")
        link = get_first_link()
        link_dict = model_to_dict(link)
        link_dict['created_at'] = date_format(link.created_at.astimezone(), format='DATETIME_FORMAT') if link.created_at else 'N/A'
        link_dict['updated_at'] = date_format(link.updated_at.astimezone(), format='DATETIME_FORMAT') if link.updated_at else 'N/A'
        link_dict['verified_at'] = date_format(link.verified_at.astimezone(), format='DATETIME_FORMAT') if link.verified_at else 'N/A'
        logger.info(f"verify_telegram - Data: {link_dict} -----------------")
        if link.id:
            tasks.verify_telegram.delay(link.id)


class DeleteInvalidLinks(CronJobBase):
    schedule = Schedule(run_at_times=['13:00'])
    code = 'ims.cron.DeleteInvalidLinks'  # 一个唯一的代码
    allow_parallel_runs = False  # 防止任务重叠，如果上一个任务实例仍在运行，新的实例将不会启动

    def do(self):
        logger.info("CronJob:DeleteInvalidLinks start -----------------")
        Link.objects.verified_and_invalid().delete()
