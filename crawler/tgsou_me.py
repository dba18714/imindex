import logging
import random
import re
import xml.etree.ElementTree as ET

import requests

logger = logging.getLogger('django')


def get_telegram_urls(url='https://tgsou.me/sitemap.xml'):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        logger.info("get_telegram_urls start -----------------")

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 将触发 HTTPError，如果响应状态码不是 200

        xml_data = response.text.strip()

        # 解析 XML 数据
        root = ET.fromstring(xml_data)

        # 提取所有的 <loc> 标签
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [url.text for url in root.findall('.//ns:loc', namespaces)]

        telegram_urls = []
        pattern = re.compile(r'/detail/(.*?)\.html')
        for url in urls:
            match = pattern.search(url)
            if match:
                telegram_url = 'https://t.me/' + match.group(1)
                telegram_urls.append(telegram_url)

        random.shuffle(telegram_urls)
        logger.info("get_telegram_urls done -----------------")
        return telegram_urls

    except requests.RequestException as e:
        logger.error(f"请求错误: {e}")
    except ET.ParseError as e:
        logger.error(f"XML 解析错误: {e}")
    except Exception as e:
        logger.error(f"未预期的错误: {e}")

    return []
