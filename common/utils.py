import re
from collections import Counter

import jieba


# 从字符串中提取URL
def extract_url_of_str(text):
    url_pattern = r'https?://[^\s]+'
    match = re.search(url_pattern, text)
    if match:
        return match.group(0)
    return None


# 从文本中提取关键词
def extract_keywords(text):

    # 使用正则表达式去除标点符号和非文字字符
    text = re.sub(r'[^\w\s]', '', text)

    # 使用 jieba 进行中文分词
    words = list(jieba.cut(text))

    # 移除空白项
    words = [item for item in words if item.strip()]

    # 计算词频
    word_counts = Counter(words)

    # 获取按最常见的词汇排序
    most_common_words = [word for word, count in word_counts.most_common()]

    return most_common_words
