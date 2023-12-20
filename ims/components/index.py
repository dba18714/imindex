import time

from django.db.models import Q
from django_unicorn.components import UnicornView
from django.core.paginator import Paginator
from ..models import Link


class IndexView(UnicornView):
    links = []
    page = 1
    query = ''
    all_articles_loaded = False  # 新增一个属性来标记是否所有文章都已加载

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.links = []
        self.query = self.request.GET.get(key='q', default='')
        self.all_articles_loaded = False
        self.load_links()

    # def load_links(self):
    #     if self.query:
    #         links = (Link.objects.verified_and_valid().order_by('-id')
    #                  .filter(Q(name__icontains=self.query) | Q(description__icontains=self.query)))
    #     else:
    #         links = Link.objects.verified_and_valid().order_by('-id').all()
    #
    #     paginator = Paginator(links, 10)  # 每页 10 项
    #     total_pages = paginator.num_pages  # 获取总页数
    #
    #     if self.page <= total_pages:
    #         page_obj = paginator.page(self.page)
    #         self.links.extend(page_obj.object_list)
    #     else:
    #         self.all_articles_loaded = True  # 如果当前页面超过总页数，标记为所有文章都已加载
    #
    #     # 在初次加载时判断是否已加载全部
    #     if self.page == 1 and total_pages <= 1:
    #         self.all_articles_loaded = True

    def load_links(self):
        max_pages = 30  # 定义允许最大页数为30

        if self.query:
            links_query = (Link.objects.verified_and_valid().order_by('-id')
                           .filter(Q(name__icontains=self.query) | Q(description__icontains=self.query)))
        else:
            links_query = Link.objects.verified_and_valid().order_by('-id').all()

        paginator = Paginator(links_query, 10)  # 每页 10 项
        total_pages = paginator.num_pages  # 获取总页数

        # 计算截止当前页的所有数据的索引范围
        start_index = 0
        end_index = self.page * 10

        # 检查当前页码是否超过了最大页数限制
        if self.page > max_pages:
            self.all_articles_loaded = True
            return

        if self.page <= total_pages:
            # 获取从第一页到当前页的所有数据
            self.links = links_query[start_index:end_index]
        else:
            # 如果当前页面超过总页数，标记为所有文章都已加载
            self.all_articles_loaded = True

        # 在初次加载时判断是否已加载全部
        if self.page == 1 and total_pages <= 1:
            self.all_articles_loaded = True

    def load_more(self):
        # time.sleep(1)
        if not self.all_articles_loaded:
            self.page += 1
            self.load_links()
        # 如果所有文章已加载，则不再增加页码
