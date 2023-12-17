import time

from celery import shared_task


@shared_task
def verified_telegram(link_id):
    from ims.models import Link
    time.sleep(10)
    link = Link.objects.get(id=link_id)
    link.verified_telegram()
    return 'Done'
