import random
import re
import xml.etree.ElementTree as ET

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


def get_telegram_urls(url='https://tgsou.me/sitemap.xml'):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        xml_data = response.text
        xml_data = xml_data.strip()

        # 解析 XML 数据
        root = ET.fromstring(xml_data)

        # 提取所有的 <loc> 标签
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}  # 定义命名空间
        urls = [url.text for url in root.findall('.//ns:loc', namespaces)]  # 使用命名空间查找

        telegram_urls = []
        pattern = re.compile(r'/detail/(.*?)\.html')
        for url in urls:
            match = pattern.search(url)
            if match:
                telegram_url = 'https://t.me/'+match.group(1)
                telegram_urls.append(telegram_url)

        # 打乱列表
        random.shuffle(telegram_urls)
        return telegram_urls

        # print("找到的 username 数量:", len(telegram_urls))
        # print(telegram_urls)


if __name__ == '__main__':
    get_telegram_urls()
