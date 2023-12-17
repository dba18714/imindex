import time

from celery import shared_task
from django.utils.autoreload import logger


@shared_task
def verified_telegram(link_id):
    logger.error(f"verified_telegram start")
    from ims.models import Link
    # time.sleep(10)
    link = Link.objects.get(id=link_id)
    link.verified_telegram()
    logger.error(f"verified_telegram Done")
    return 'Done'
