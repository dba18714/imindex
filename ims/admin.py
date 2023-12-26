from django.contrib import admin, messages
from django.template.defaultfilters import truncatechars
from django.utils.formats import date_format
from django.utils.html import format_html

from . import tasks
from .models import Link
from django.utils.translation import gettext_lazy as _


def action_verify_telegram(modeladmin, request, queryset):
    for obj in queryset:
        tasks.verify_telegram.delay(obj.id)

    modeladmin.message_user(request, '成功在后台执行了验证 Telegram URL 操作', messages.SUCCESS)


action_verify_telegram.short_description = '验证 Telegram URL'


class Admin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ["show_name", "show_description", "member_count", "show_url", "show_time"]
    list_filter = ["is_valid", "verified_at"]
    search_fields = ["id", "uuid", "name", "description", "member_count", "url"]
    actions = [action_verify_telegram]

    def show_url(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url, obj.url)

    show_url.short_description = 'url'

    def show_description(self, obj):
        return truncatechars(obj.description, 50)

    show_description.short_description = Link._meta.get_field('description').verbose_name

    def show_name(self, obj):
        return truncatechars(obj.name, 20)

    show_name.short_description = Link._meta.get_field('name').verbose_name
    show_name.admin_order_field = 'name'

    def show_time(self, obj):
        created_at = date_format(obj.created_at.astimezone(), format='DATETIME_FORMAT') if obj.created_at else 'N/A'
        updated_at = date_format(obj.updated_at.astimezone(), format='DATETIME_FORMAT') if obj.updated_at else 'N/A'
        verified_at = date_format(obj.verified_at.astimezone(), format='DATETIME_FORMAT') if obj.verified_at else 'N/A'
        return format_html('<div style="white-space: nowrap;">创建于 {}<br>更新于 {}<br>验证于 {}</div>',
                           created_at, updated_at, verified_at)

    show_time.short_description = _('time')


admin.site.register(Link, Admin)
