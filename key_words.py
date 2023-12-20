# # import jieba
# # from gensim.summarization import keywords
# #
# # text = "您的中文文本数据放在这里..."
# # words = " ".join(jieba.cut(text))
# #
# # # 提取关键词
# # key_words = keywords(words).split('\n')
# # print(key_words)
# import re
# from urllib.parse import quote
#
# import jieba
# from collections import Counter
#
# import requests
# from bs4 import BeautifulSoup
#
#
# def main():
#
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
#     }
#
#     # response = requests.get('https://www.tgcng.com/', headers=headers)
#     # response = requests.get('https://www.tgcng.com/tags.php', headers=headers)
#     response = requests.get('https://www.playpcesor.com/2020/01/telegram-20.html', headers=headers)
#
#     if response.status_code == 200:
#         # 解析 HTML
#         soup = BeautifulSoup(response.text, 'lxml')
#
#         # 提取文本
#         text = soup.get_text(separator=' ', strip=True)
#
#         # 使用正则表达式去除标点符号和非文字字符
#         text = re.sub(r'[^\w\s]', '', text)
#
#         # text = response.text
#         # text = "您的中文文本数据放在这里..."
#
#         # 使用 jieba 进行分词
#         words = list(jieba.cut(text))
#
#         # 计算词频
#         word_counts = Counter(words)
#
#         # 获取最常见的词
#         most_common_words = word_counts.most_common(1000)
#         for word, word_count in most_common_words:
#             info_ids = get_info_ids(word)
#             print(word)
#         print(most_common_words)
#         if most_common_words:
#             print(most_common_words[2][0])  # 如果列表不为空，则打印第一个元素
#         else:
#             print("没有找到常见单词")
#         print(len(most_common_words))
#
#         info_ids = get_info_ids(most_common_words[2][0])
#         if not info_ids:
#             print(info_ids, 'not')
#
#         print(info_ids)
#         print(len(info_ids))
#
#         # for word, word_count in most_common_words:
#         #     print(word)
#         # print(most_common_words)
#         # if most_common_words:
#         #     print(most_common_words[2][0])  # 如果列表不为空，则打印第一个元素
#         # else:
#         #     print("没有找到常见单词")
#         # print(len(most_common_words))
#         #
#         # info_ids = get_info_ids(most_common_words[2][0])
#         # if not info_ids:
#         #     print(info_ids, 'not')
#         #
#         # print(info_ids)
#         # print(len(info_ids))
#         #
#
#
# def get_info_ids(tag):
#
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
#     }
#
#     # response = requests.get('https://www.tgcng.com/', headers=headers)
#     response = requests.get(f'https://www.tgcng.com/tag.php?k={quote(tag)}', headers=headers)
#
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'lxml')
#
#         # 查找所有的 a 标签
#         a_tags = soup.find_all('a', href=True)
#
#         # 正则表达式匹配 gid
#         gid_pattern = re.compile(r'gid=(\d+)')
#
#         # 创建一个空列表来存储 gid 值
#         gids = []
#
#         # 提取所有的 gid 值并添加到列表中
#         for tag in a_tags:
#             href = tag['href']
#             match = gid_pattern.search(href)
#             if match:
#                 gid = match.group(1)
#                 gids.append(gid)
#
#         # 打印所有的 gid 值
#         return gids
#
#
# if __name__ == '__main__':
#     main()
