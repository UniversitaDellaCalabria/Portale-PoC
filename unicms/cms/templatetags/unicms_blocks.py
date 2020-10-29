import logging

from django import template
from django.conf import settings
from django.template.loader import get_template, render_to_string
from django.template.exceptions import (TemplateDoesNotExist,
                                        TemplateSyntaxError)
from django.utils import timezone
from django.utils.safestring import mark_safe
# WARNING - import circolare - decidere di migrare blocchi e menu in cms_pages
from cms.models import NavigationBarItem
from cms.views import detect_user_language

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def supported_languages():
    return settings.LANGUAGES


@register.simple_tag(takes_context=True)
def load_menus(context, section, template):
    _error_msg = 'ERROR: unicms_blocks template tags load_menus: {}'
    _error_msg_pub = '<!-- Error load_menus template tags. See log file. -->'

    request = context['request']
    language = detect_user_language(request)

    menu = NavigationBarItem.objects.filter(section=section,
                                            is_active=True,
                                            parent__isnull=True).\
                                     order_by('order')
    # i18n override
    for i in menu:
        #  import pdb; pdb.set_trace()
        i18n = i.navigationbaritemlocalization_set.filter(language=language).first()
        if i18n:
            i.name = i18n.name
    #

    data = {
            'context': context,
            'menu': menu
    }
    try:
        return render_to_string(template, data)
    except TemplateDoesNotExist as e:
        logger.error(_error_msg.format(e))
    except TemplateSyntaxError as e:
        logger.error(_error_msg.format(e))

    return mark_safe(_error_msg_pub)


# @register.simple_tag(takes_context=True)
# def load_blocks(context, template):
    # t = get_template(template)
