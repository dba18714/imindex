# services.py
import logging
import pprint
import re

import requests
from bs4 import BeautifulSoup
from django.utils.timezone import now

# from django.utils.autoreload import logger
logger = logging.getLogger('django')


def verify_telegram(link_id):
    from ims.models import Link
    try:
        link = Link.objects.get(id=link_id)
        url = link.url
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')

            # 提取 Telegram 名称和描述
            telegram_name = soup.select_one('.tgme_page_title span')
            link.name = telegram_name.text if telegram_name else 'none'

            telegram_description = soup.select_one('.tgme_page_description')
            link.description = telegram_description.text if telegram_description else 'none'

            telegram_member_count = soup.select_one('.tgme_page_extra')
            if telegram_member_count:
                match = re.search(r'(\d[\d\s,]*)members', telegram_member_count.text)
                if match:
                    link.member_count = int(re.sub(r'\D', '', match.group(1)))
                    link.category = link.GROUP
                match = re.search(r'(\d[\d\s,]*)subscribers', telegram_member_count.text)
                if match:
                    link.member_count = int(re.sub(r'\D', '', match.group(1)))
                    link.category = link.CHANNEL
                match = re.search(r'^@\w+$', telegram_member_count.text)
                if match:
                    link.category = link.PERSONAL

            # 检查是否有效
            link.is_valid = True
            robots_meta = soup.find('meta', attrs={'name': 'robots'})
            if robots_meta and robots_meta.get('content') != 'none':
                link.is_valid = False

            link.verified_at = now()
            link.save()

        else:
            # 记录错误日志
            logger.error("HTTP 请求失败" + pprint.pformat({
                'URL': url,
                'status': response.status_code,
                'headers': response.headers,
                'body': response.text,
            }, indent=4))

    except Exception as e:
        logger.error(f"发生异常: {e}")
