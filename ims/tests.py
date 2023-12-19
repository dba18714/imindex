import uuid

from django.test import TestCase
from django.utils import timezone

from .models import Link
from .cron import DeleteInvalidLinks


class DeleteInvalidLinksTest(TestCase):
    def setUp(self):
        # 创建测试数据
        Link.objects.create(verified_at=timezone.now(), is_valid=False, url=f"https://x.com/{uuid.uuid4()}")
        Link.objects.create(verified_at=timezone.now(), is_valid=False, url=f"https://x.com/{uuid.uuid4()}")
        Link.objects.create(verified_at=timezone.now(), is_valid=True, url=f"https://x.com/{uuid.uuid4()}")
        Link.objects.create(verified_at=timezone.now(), is_valid=True, url=f"https://x.com/{uuid.uuid4()}")

    def test_delete_invalid_links(self):
        self.assertEqual(Link.objects.verified_and_invalid().count(), 2)

        # 执行定时任务
        job = DeleteInvalidLinks()
        job.do()

        # 验证结果
        self.assertFalse(Link.objects.verified_and_invalid().exists())
        self.assertEqual(Link.objects.count(), 2)
