from django.contrib.sitemaps import Sitemap
from .models import Link


class LinkSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    limit = 1000

    def items(self):
        return Link.objects.verified_and_valid().all()

    def lastmod(self, obj):
        return obj.updated_at
