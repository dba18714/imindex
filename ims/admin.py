from collections import defaultdict
import logging

from django.contrib import admin, messages
from django.template.defaultfilters import truncatechars
from django.urls import path
from django.utils.formats import date_format
from django.utils.html import format_html

from . import tasks
from .models import Ad, Link, Search
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger('django')


def action_verify_telegram(modeladmin, request, queryset):
    for obj in queryset:
        tasks.verify_telegram_dispatch(obj.id)
        logger.info(f"action_verify_telegram link_id: {obj.id} -----------------")

    modeladmin.message_user(request, '成功在后台执行了验证 Telegram URL 操作', messages.SUCCESS)


action_verify_telegram.short_description = '验证 Telegram URL'


from django.http import HttpResponseRedirect



def clear_redis(request):
    import redis
    r = redis.Redis(host='redis', password='RDFGDxpI1h', port=6379, db=0)
    # r.flushdb() # 清除当前数据库
    r.flushall() # 清除所有数据库

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LinkAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('clear-redis/', self.admin_site.admin_view(clear_redis), name='clear-redis'),
        ]
        return custom_urls + urls
    
    list_per_page = 50
    list_display = ["id", "show_name", "member_count", "show_url", "verified_start_at", "verified_at", "created_at"]
    list_filter = ["is_by_user", "is_valid", "verified_start_at", "verified_at", "created_at"]
    search_fields = ["id", "uuid", "name", "description", "member_count", "url"]
    actions = [action_verify_telegram]

    def show_url(self, obj):
        return format_html(f'<a href="{obj.url}" target="_blank">{obj.url}</a>')

    show_url.short_description = 'url'
    show_url.admin_order_field = 'url'

    # def show_description(self, obj):
    #     return truncatechars(obj.description, 50)
    #
    # show_description.short_description = Link._meta.get_field('description').verbose_name

    def show_name(self, obj):
        # return format_html('%s<br><span style="font-size: 12px;">介绍：%s</span>' %
        #                    (truncatechars(obj.name, 20), truncatechars(obj.description, 20)))
        name = obj.name.replace("{", "{{").replace("}", "}}")
        description = obj.description.replace("{", "{{").replace("}", "}}")
        return format_html(f'{truncatechars(name, 20)}<br>'
                           f'<span style="font-size: 12px;">介绍：{truncatechars(description, 20)}</span>')
        # return truncatechars(obj.name, 20)

    show_name.short_description = Link._meta.get_field('name').verbose_name
    show_name.admin_order_field = 'name'

    # def show_time(self, obj):
    #     created_at = date_format(obj.created_at.astimezone(), format='DATETIME_FORMAT') if obj.created_at else 'N/A'
    #     updated_at = date_format(obj.updated_at.astimezone(), format='DATETIME_FORMAT') if obj.updated_at else 'N/A'
    #     verified_at = date_format(obj.verified_at.astimezone(), format='DATETIME_FORMAT') if obj.verified_at else 'N/A'
    #     return format_html('<div style="white-space: nowrap;">创建于 {}<br>更新于 {}<br>验证于 {}</div>',
    #                        created_at, updated_at, verified_at)
    #
    # show_time.short_description = _('time')


admin.site.register(Link, LinkAdmin)


class SearchAdmin(admin.ModelAdmin):
    list_display = ["id", "keyword", "search_count", "created_at", "last_search_at"]

admin.site.register(Search, SearchAdmin)


class AdAdmin(admin.ModelAdmin):
    list_display = ["id", "status", "title", "display_places", "image", "click_count", "created_at", "start_at", "end_at"]

    def display_places(self, obj):
        return " + ".join([place.name for place in obj.place.all()])  # 获取所有 place 名称并以逗号分隔

    display_places.short_description = '展示位置'  # 自定义列的标题


admin.site.register(Ad, AdAdmin)

