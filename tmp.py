# import threading
# import time

# # 创建一个Lock对象
# lock = threading.Lock()

# def verify_telegram_synchronized(link_id):
#     # 获取锁
#     lock.acquire()
#     try:
#         # 执行需要同步的代码
#         print("333333333333333")
#         time.sleep(20)
#     finally:
#         # 无论是否发生错误，都要释放锁
#         lock.release()

# verify_telegram_synchronized(1)

# exit()


import os
import random
import time

import django
from django.db.models import F

from ims.tasks import get_or_create_link

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# 初始化 Django
django.setup()

from ims.models import Link
from crawler.tgcng_com import get_words, get_info_ids, get_telegram_url, get_words_by_db



import redis
from redis.lock import Lock

# 创建一个Redis连接
r = redis.Redis(host='redis', port=6379, db=0, password='RDFGDxpI1h')

# 创建一个锁
lock = r.lock('my_lock')

# 获取锁
lock.acquire(blocking=True)

# 在这里执行你的代码
print("7865432243565787666666666")
time.sleep(20)

# 释放锁
lock.release()

exit()

from django.db import transaction

def verify_telegram_synchronized(link_id):
    # 获取数据库锁
    with transaction.atomic():
        # 执行需要同步的代码
        print("333333333333333")
        time.sleep(20)

verify_telegram_synchronized(1)

exit()

# print("33333333333")
# # 获取5条Link
# links = Link.objects.order_by("id").all()[:5]
# print(links)
# exit()


print("33333333333")
words = get_words_by_db()
print(words)
for word in words:
    print(word)
print("get_words_by_db()")
exit()

urls = [
    # 'https://www.tgcng.com/tags.php',
    # 'https://github.com/itgoyo/TelegramGroup',
    # 'https://github.com/jackhawks/rectg',
    'https://s.weibo.com/top/summary',
]
url = random.choice(urls)
get_words = get_words(url=url)
print(get_words)
exit()

link, created = get_or_create_link('https://tnav.me/22')
print(link.id, created)
exit()

links = Link.objects.order_by(F('verified_at').asc(nulls_first=True), 'created_at')[:3]

for link in links:
    print(link.id)

links_list = list(links)
print(links_list)

# 对列表进行随机排序
random.shuffle(links_list)

# 打印随机排序后的顺序
for link in links_list:
    print(link.id)
