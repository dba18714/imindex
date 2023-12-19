from django.contrib import admin

from .models import Link


class Admin(admin.ModelAdmin):
    list_display = ["name", "description", "member_count", "url"]
    list_filter = ["uuid", "name"]
    search_fields = ["uuid", "name", "description", "member_count", "url"]


admin.site.register(Link, Admin)
