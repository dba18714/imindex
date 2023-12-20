from django import template
from django.utils.translation import get_language

register = template.Library()


@register.simple_tag
def get_lang_code():
    current_lang = get_language()
    return current_lang.replace('zh-hans', 'zh-CN')
