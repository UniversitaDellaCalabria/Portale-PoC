import logging

from django import template
from django.conf import settings
from django.template.loader import get_template, render_to_string
from django.template.exceptions import (TemplateDoesNotExist,
                                        TemplateSyntaxError)
from django.utils import timezone
from django.utils.safestring import mark_safe
from cms_context.utils import detect_user_language

from cms_menus.models import NavigationBar, NavigationBarItem


logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(takes_context=True)
def load_menus(context, section, template):
    _error_msg = 'ERROR: unicms_blocks template tags load_menus: {}'
    _error_msg_pub = '<!-- Error load_menus template tags. See log file. -->'

    request = context['request']
    language = detect_user_language(request)

    menu = NavigationBar.objects.filter(section=section,
                                        is_active=True,
                                        context=context['context']).first()
    menu_items = NavigationBarItem.objects.filter(menu=menu,
                                                  is_active=True,
                                                  parent__isnull=True).\
                                           order_by('order')
    # i18n override
    for i in menu_items:
        #  import pdb; pdb.set_trace()
        i18n = i.navigationbaritemlocalization_set.filter(language=language).first()
        if i18n:
            i.name = i18n.name
    #

    data = {
            'context': context,
            'menu': menu_items
    }
    try:
        return render_to_string(template, data)
    except TemplateDoesNotExist as e:
        logger.error(_error_msg.format(e))
    except TemplateSyntaxError as e:
        logger.error(_error_msg.format(e))

    return mark_safe(_error_msg_pub)
