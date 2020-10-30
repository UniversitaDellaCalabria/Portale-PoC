import logging

from django import template
from django.conf import settings
from django.template.loader import get_template, render_to_string
from django.template.exceptions import (TemplateDoesNotExist,
                                        TemplateSyntaxError)
from django.utils import timezone
from django.utils.safestring import mark_safe
from cms_context.decorators import detect_language
from cms_context.utils import handle_faulty_templates

from cms_menus.models import NavigationBar, NavigationBarItem


logger = logging.getLogger(__name__)
register = template.Library()


@detect_language
@register.simple_tag(takes_context=True)
def load_menus(context, section, template):
    request = context['request']
    menu = NavigationBar.objects.filter(section=section,
                                        is_active=True,
                                        context=context['context']).first()
    menu_items = NavigationBarItem.objects.filter(menu=menu,
                                                  is_active=True,
                                                  parent__isnull=True).\
                                           order_by('order')
    # i18n override
    language = request.LANGUAGE_CODE
    for i in menu_items:
        i18n = i.navigationbaritemlocalization_set.filter(language=language).first()
        if i18n:
            i.name = i18n.name
    #
    data = {'menu': menu_items}
    return handle_faulty_templates(template, data, name='load_menus')
