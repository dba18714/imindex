import uuid
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from crawler.tgcng_com import get_words, get_info_ids, get_telegram_url
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


class GetWordsTest(TestCase):
    @patch('crawler.tgcng_com.requests.get')
    def test_get_words(self, mock_get):
        # 设置模拟响应
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '當我們的電腦使用久了遇到問題時，有時僅需重啟即可解決。同樣地，我們的大腦和自身行為模式也可能需要類似的「重新開機」。雖然大多數人（包括我自己）無法徹底重置自己的生活或環境， 但通過一些簡單的方法來讓大腦或某些負面習慣重啟，可以是重新獲得動力、恢復生產力，以及打破惡性循環的有效途徑。'

        # 调用函数
        words = get_words()

        # 断言
        self.assertIsInstance(words, list)
        self.assertIn('開機', words)


class GetInfoIdsTest(TestCase):
    @patch('crawler.tgcng_com.requests.get')
    def test_get_info_ids(self, mock_get):
        # 设置模拟响应
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '''<a href="info.php?gid=3984589" class="item" data-v-939db994>
<img src="logo/3984589.jpg" class="icon" data-v-939db994 />
<div class="info" data-v-939db994>
<div class="name" data-v-939db994> 16.🌈东南亚金三角总部交流群👑 </div>
<div class="intro1" data-v-939db994>
<span data-v-939db994>114.5k 用户</span>
<span class="space" data-v-939db994>I</span>
<span class="updatime" data-v-939db994>2023-11-11</span>
</div>
<div class="intro2" data-v-939db994> 欢迎加入金三角总部交流群 这是梦开始的地方，</div>
</div>
<div class="join" data-v-939db994> 查看 </div>
</a>'''

        # 调用函数
        ids = get_info_ids('测试')

        # 断言
        self.assertIsInstance(ids, list)
        self.assertIn('3984589', ids)


class GetTelegramUrlTest(TestCase):
    @patch('crawler.tgcng_com.scrape_with_xpath')
    def test_get_telegram_url(self, mock_scrape):
        # 设置模拟响应
        mock_scrape.return_value = ['手机扫码入群：https://t.me/xxx']

        # 调用函数
        url = get_telegram_url('123')

        # 断言
        self.assertIsInstance(url, str)
        self.assertEqual(url, 'https://t.me/xxx')
