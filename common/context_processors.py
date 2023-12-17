from django.conf import settings
from django.templatetags.i18n import do_get_available_languages
from django.utils.translation import get_language_info


def my_custom_context(request):
    current_language_info = get_language_info(request.LANGUAGE_CODE)

    languages = []
    for code, name in settings.LANGUAGES:
        lang_info = get_language_info(code)
        languages.append({
            'code': code,
            'name': lang_info['name'],
            'local_name': lang_info['name_local']
        })

    return {
        'languages': languages,
        'current_language_info': current_language_info,
    }
