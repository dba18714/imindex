"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.views import serve
from django.urls import path, include, re_path
from django.http import HttpResponsePermanentRedirect

from ims.sitemaps import LinkSitemap

sitemaps = {
    'link': LinkSitemap,
}

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('admin/', admin.site.urls),
    path("", include("ims.urls")),
    path("polls/", include("polls.urls")),
    path("unicorn/", include("django_unicorn.urls")),

    # 其他路径配置
    path('i18n/', include('django.conf.urls.i18n')),  # 如果不需要 i18n 功能，可以移除这一行
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
] 

# 添加静态文件的 URL
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 重定向旧版本带语言代码的URL，包括首页
urlpatterns += [
    path('en/', lambda request: HttpResponsePermanentRedirect("/")),
    path('zh-hans/', lambda request: HttpResponsePermanentRedirect("/")),
    path('en/<path:subpath>/', lambda request, subpath: HttpResponsePermanentRedirect(f"/{subpath}")),
    path('zh-hans/<path:subpath>/', lambda request, subpath: HttpResponsePermanentRedirect(f"/{subpath}")),
]