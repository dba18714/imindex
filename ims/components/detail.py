import time

from django.db.models.expressions import RawSQL
from django_unicorn.components import UnicornView
from django.core.paginator import Paginator
from ..models import Link


class DetailView(UnicornView):
    hot_links = Link.objects.verified_and_valid().order_by('-member_count')[:5]
    random_links = Link.objects.verified_and_valid().annotate(
        random_order=RawSQL('RANDOM()', [])
    ).order_by('random_order')[:5]
