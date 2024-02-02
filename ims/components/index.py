import time

from django.db.models import Q
from django_unicorn.components import UnicornView
from django.core.paginator import Paginator
from ..models import Link, Search


def update_search_statistics(query):
    """更新搜索统计数据。"""
    search, created = Search.objects.get_or_create(keyword=query)
    search.search_count += 1
    search.save()


class IndexView(UnicornView):
    links = []
    page = 1
    query = ''
    top_searches = []
    all_articles_loaded = False  # 新增一个属性来标记是否所有文章都已加载

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.top_searches = Search.objects.order_by('-search_count')[:15]
        self.links = []
        self.query = self.request.GET.get(key='q', default='').strip()
        self.all_articles_loaded = False
        self.load_links()

    def load_links(self):
        max_pages = 30  # 定义允许最大页数为30
        per_page = 20

        links_query = Link.objects.verified_and_valid().order_by('-id')
        if self.query:
            update_search_statistics(self.query)
            links_query = links_query.filter(Q(name__icontains=self.query) |
                                             Q(description__icontains=self.query) |
                                             Q(url__icontains=self.query))

        paginator = Paginator(links_query, per_page)  # 每页 N 项

        # 计算截止当前页的所有数据的索引范围
        start_index = 0
        end_index = self.page * per_page

        if self.page > max_pages or self.page > paginator.num_pages:
            self.all_articles_loaded = True
            return

        self.links = links_query[start_index:end_index]

        # 在初次加载时判断是否已加载全部
        if self.page == 1 and paginator.num_pages <= 1:
            self.all_articles_loaded = True

    def load_more(self):
        # time.sleep(1)
        if not self.all_articles_loaded:
            self.page += 1
            self.load_links()
        # 如果所有文章已加载，则不再增加页码
