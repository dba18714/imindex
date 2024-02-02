from django import template
from django.conf import settings
from django.templatetags.i18n import do_get_available_languages
from django.utils.translation import get_language_info

register = template.Library()

# LANGUAGE_ENGLISH_NAMES = dict(settings.LANGUAGES)

# languages = []
# for lang_code in do_get_available_languages():
#     lang_info = get_language_info(lang_code)
#     languages.append({
#         'code': lang_code,
#         'name': lang_info['name'],
#         'local_name': lang_info['name_local']
#     })
#
#
# @register.simple_tag
# def get_language_english_name(language_code):
#     return languages.get(language_code, language_code)
