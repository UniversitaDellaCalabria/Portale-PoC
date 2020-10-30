from django.conf import settings
from django.utils import translation


def detect_user_language(request):
    lang = request.GET.get('lang',
                           translation.get_language_from_request(request))
    translation.activate(lang)
    request.LANGUAGE_CODE = translation.get_language()
    return lang
