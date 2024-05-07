import logging
import random
import re
import time
from urllib.parse import quote

import jieba
from collections import Counter

import requests
from bs4 import BeautifulSoup
import common.utils
from common.utils import extract_keywords

from crawler.spiders.spider import scrape_with_xpath
from django.db.models.expressions import RawSQL

from ims.services import get_or_create_link


logger = logging.getLogger('django')

class Run:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 记录开始时间和允许的最大运行时间
        self.start_time = time.time()
        self.max_minutes = 1

    # 是否超时
    def is_timeout(self):
        return time.time() - self.start_time > self.max_minutes * 60

    def check_timeout(self):
        if self.is_timeout():
            # logger.info("Command: runspider timeout -----------------")
            return True
        return False

    def random_sleep(self, num_a, num_b):
        time.sleep(random.uniform(num_a, num_b))

    def handle(self, *args, **kwargs):
        # logger.info("Command: runspider start -----------------")
        # return

        num_a = 0.2
        num_b = 1.0
        # for word in get_words():
        # urls = [
        #     'https://www.tgcng.com/tags.php',
        #     'https://github.com/itgoyo/TelegramGroup',
        #     'https://github.com/jackhawks/rectg',
        #     'https://s.weibo.com/top/summary',
        # ]
        # url = random.choice(urls)
        # words = get_words(url=url)
        words = get_words_by_db()
        for word in words[:100]:

            if self.check_timeout():
                return

            ids = get_info_ids(word)
            for info_id in ids[:100]:

                if self.check_timeout():
                    return

                telegram_url = get_telegram_url(info_id)
                if telegram_url:
                    get_or_create_link(url=telegram_url)

                self.random_sleep(num_a, num_b)
            self.random_sleep(num_a, num_b)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

def get_words_by_db():
    # 随机获取5条Link
    from ims.models import Link
    # links = Link.objects.verified_and_valid().order_by('?')[:10]
    links = Link.objects.verified_and_valid().annotate(
            random_order=RawSQL('RANDOM()', [])
        ).order_by('random_order')[:10]
    str = ''
    for link in links:
        s= link.name + ' ' + link.description + ' '
        s = s.replace('none', '') # 删除‘none’字符
        str += s

    words = extract_keywords(str)

    # # 删除以‘http’开头的词
    # words = [word for word in words if not word.startswith('http')]

    # # 删除全字母的词，用正则表达式
    # words = [word for word in words if not re.match(r'^[a-zA-Z]+$', word)]
    
    # # 删除全数字的词
    # words = [word for word in words if not word.isdigit()]

    # 删除长度小于2的词
    words = [word for word in words if len(word) > 1]

    # 删除非中文的词
    words = [word for word in words if re.match(r'^[\u4e00-\u9fa5]+$', word)]

    # 打乱列表
    random.shuffle(words)
    
    return words


def get_words(url='https://www.tgcng.com/tags.php'):
    try:

        response = requests.get(url, headers=headers)

        response.raise_for_status()  # 将触发 HTTPError，如果响应状态码不是 200

        # 解析 HTML
        soup = BeautifulSoup(response.text, 'lxml')

        # 提取文本
        text = soup.get_text(separator=' ', strip=True)

        # # 使用正则表达式去除标点符号和非文字字符
        # text = re.sub(r'[^\w\s]', '', text)1
        #
        # # text = response.text
        # # text = "您的中文文本数据放在这里..."
        #
        # # 使用 jieba 进行分词
        # words = list(jieba.cut(text))1
        #
        # # 过滤掉空白字符
        # words = [item for item in words if item.strip()]1
        #
        # # 计算词频
        # word_counts = Counter(words)1
        #
        # # 获取最常见的词
        # most_common_words = word_counts.most_common()1
        #
        # words = []1
        #
        # # 提取所有的 gid 值并添加到列表中
        # for v, word_count in most_common_words:1
        #     words.append(v)1

        words = extract_keywords(text)

        # 打乱列表
        random.shuffle(words)
        return words
        # print(words)

    except requests.RequestException as e:
        logger.error(f"请求错误: {e}")
    except Exception as e:
        logger.error(f"未预期的错误: {e}")

    return []


def get_info_ids(tag):
    try:
        # response = requests.get('https://www.tgcng.com/', headers=headers)
        response = requests.get(f'https://www.tgcng.com/tag.php?k={quote(tag)}', headers=headers)

        response.raise_for_status()  # 将触发 HTTPError，如果响应状态码不是 200

        soup = BeautifulSoup(response.text, 'lxml')

        # 查找所有的 a 标签
        a_tags = soup.find_all('a', href=True)

        # 正则表达式匹配 gid
        gid_pattern = re.compile(r'gid=(\d+)')

        # 创建一个空列表来存储 gid 值
        gids = []

        # 提取所有的 gid 值并添加到列表中
        for tag in a_tags:
            href = tag['href']
            match = gid_pattern.search(href)
            if match:
                gid = match.group(1)
                gids.append(gid)

        # 打乱列表
        random.shuffle(gids)
        return gids

    except requests.RequestException as e:
        logger.error(f"请求错误: {e}")
    except Exception as e:
        logger.error(f"未预期的错误: {e}")

    return []


def get_telegram_url(info_id):
    try:
        url = f"https://www.tgcng.com/info.php?gid={info_id}"
        xpath = '/html/body/div[@id="__nuxt"]/div[@id="__layout"]/div[@id="app"]/div[@class="container"]/div[@class="info"]/a[@class="item"]/div[@class="member"]'

        text_contents = scrape_with_xpath(url, xpath)
        if not text_contents:
            return None
        telegram_url = common.utils.extract_url_of_str(text_contents[0])
        return telegram_url

    except requests.RequestException as e:
        logger.error(f"请求错误: {e}")
    except Exception as e:
        logger.error(f"未预期的错误: {e}")

    return None


if __name__ == '__main__':
    print(get_words_by_db())
    exit()
    i = 0
    for word in get_words():
        i += 1
        ids = get_info_ids(word)
        print(ids)
        for info_id in ids:
            i += 1
            url = get_telegram_url(info_id)
            print(url)
            if i >= 5:
                break

        if i >= 5:
            break
