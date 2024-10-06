import time

from django.db.models.expressions import RawSQL
from django_unicorn.components import UnicornView
from django.core.paginator import Paginator
from ..models import Ad, Link
from django.utils import timezone


class DetailView(UnicornView):
    hot_links = []
    random_links = []
    ads = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.now()
        self.ads = Ad.objects.filter(place=2, start_at__lte=now, end_at__gte=now).order_by('end_at')
        self.hot_links = Link.objects.verified_and_valid().order_by('-member_count')[:5]
        self.random_links = Link.objects.verified_and_valid().annotate(
            random_order=RawSQL('RANDOM()', [])
        ).order_by('random_order')[:5]
