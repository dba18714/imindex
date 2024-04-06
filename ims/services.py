# services.py
import logging
import pprint
import re

import requests
from bs4 import BeautifulSoup
from django.forms import model_to_dict
from django.utils.timezone import now

# from django.utils.autoreload import logger
logger = logging.getLogger('django')


def get_or_create_link(url, is_by_user=False):
    from ims.models import Link
    link, created = Link.objects.get_or_create(
        url__iexact=url,
        defaults={'url': url, 'is_by_user': is_by_user}  # 如果需要创建新对象，则使用这些默认值
    )
    return link, created


def verify_telegram(link_id):
    from ims.models import Link
    try:
        link = Link.objects.get(id=link_id)
        # link.verified_start_at = now()
        # link.save()

        url = link.url
        logger.info(f"verify_telegram URL：{url} - Data: {model_to_dict(link)} -----------------")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 将触发 HTTPError，如果响应状态码不是 200

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

        logger.info(f"verify_telegram URL：{url} - success -----------------")

    except requests.RequestException as e:
        logger.error(f"处理 link_id:{link_id} 时发生请求错误: {e}")
    except Exception as e:
        logger.error(f"处理 link_id:{link_id} 时发生未预期的错误: {e}")


    # else:
    #         # 记录错误日志
    #         logger.error("HTTP 请求失败" + pprint.pformat({
    #             'URL': url,
    #             'status': response.status_code,
    #             'headers': response.headers,
    #             'body': response.text,
    #         }, indent=4))
    #
    # except Exception as e:
    #     logger.error(f"处理 link_id:{link_id} 时发生异常: {e}")
