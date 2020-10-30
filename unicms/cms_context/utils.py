import logging

from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe
from django.template.loader import get_template, render_to_string
from django.template.exceptions import (TemplateDoesNotExist,
                                        TemplateSyntaxError)


logger = logging.getLogger(__name__)


def detect_user_language(request):
    lang = request.GET.get('lang',
                           translation.get_language_from_request(request))
    translation.activate(lang)
    request.LANGUAGE_CODE = translation.get_language()
    return lang


def handle_faulty_templates(template: str, data: dict, name='', ):
    _error_msg = 'ERROR: {} template tags: {}'
    _error_msg_pub = '<!-- Error {} template tags. See log file. -->'
    
    try:
        return render_to_string(template, data)
    except TemplateDoesNotExist as e:
        logger.error(_error_msg.format(name, e))
    except TemplateSyntaxError as e:
        logger.error(_error_msg.format(name, e))

    return mark_safe(_error_msg_pub)
