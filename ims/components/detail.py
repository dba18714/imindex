import time

from django_unicorn.components import UnicornView
from django.core.paginator import Paginator
from ..models import Link


class DetailView(UnicornView):
    hot_links = Link.objects.verified_and_valid().order_by('-member_count')[:5]
