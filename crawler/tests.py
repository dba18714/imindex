from django.test import TestCase
from unittest.mock import patch
from .tgsou_me import get_telegram_urls  # 确保从正确的位置导入函数


class GetTelegramUrlsTestCase(TestCase):

    @patch('crawler.tgsou_me.requests.get')  # 替换 'yourapp.views' 为实际的路径
    def test_get_telegram_urls(self, mock_get):
        # 模拟的 XML 数据
        mock_xml_data = '''
        <?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url><loc>https://tgsou.me/detail/username1.html</loc></url>
            <url><loc>https://tgsou.me/detail/username2.html</loc></url>
        </urlset>
        '''

        # 设置模拟的返回值
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = mock_xml_data

        # 调用函数并验证结果
        expected_urls = ['https://t.me/username1', 'https://t.me/username2']
        self.assertEqual(set(get_telegram_urls()), set(expected_urls))
