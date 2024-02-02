import logging
import random
import re
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup

from common.utils import extract_url_of_str
from crawler.spiders.spider import scrape_with_xpath

logger = logging.getLogger('django')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def get_telegram_urls_of_html():
    with requests.Session() as session:
        session.headers = headers
        try:
            response = session.get(f'https://tgsou.me/')
            response.raise_for_status()  # 将触发 HTTPError，如果响应状态码不是 200
            soup = BeautifulSoup(response.text, 'lxml')

            # 查找所有的 a 标签
            divs = soup.find_all('div', class_='font-13 text-success mb-3')

            telegram_urls = [div.get_text() for div in divs]

            # 打乱列表
            random.shuffle(telegram_urls)
            return telegram_urls
        except requests.RequestException as e:
            logger.error(f"请求错误: {e}")
        except ET.ParseError as e:
            logger.error(f"XML 解析错误: {e}")
        except Exception as e:
            logger.error(f"未预期的错误: {e}")

    return []


if __name__ == "__main__":
    print(len(get_telegram_urls_of_html()))


def get_telegram_urls_of_xml(url='https://tgsou.me/sitemap.xml'):
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
