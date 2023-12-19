import time

from django.db.models import Q
from django_unicorn.components import UnicornView
from django.core.paginator import Paginator
from ..models import Link


class IndexView(UnicornView):
    links = []
    page = 1
    all_articles_loaded = False  # 新增一个属性来标记是否所有文章都已加载

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.links = []
        self.all_articles_loaded = False
        self.load_links()

    def load_links(self):
        query = self.request.GET.get("q")  # 获取搜索查询参数
        if query:
            links = (Link.objects.verified_and_valid().order_by('-id')
                     .filter(Q(name__icontains=query) | Q(description__icontains=query)))
        else:
            links = Link.objects.verified_and_valid().order_by('-id').all()

        paginator = Paginator(links, 10)  # 每页 10 项
        total_pages = paginator.num_pages  # 获取总页数

        if self.page <= total_pages:
            page_obj = paginator.page(self.page)
            self.links.extend(page_obj.object_list)
        else:
            self.all_articles_loaded = True  # 如果当前页面超过总页数，标记为所有文章都已加载

        # 在初次加载时判断是否已加载全部
        if self.page == 1 and total_pages <= 1:
            self.all_articles_loaded = True

    def load_more(self):
        # time.sleep(1)
        if not self.all_articles_loaded:
            self.page += 1
            self.load_links()
        # 如果所有文章已加载，则不再增加页码
