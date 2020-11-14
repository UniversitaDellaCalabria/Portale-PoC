import logging

from django import template
from django.template.exceptions import (TemplateDoesNotExist,
                                        TemplateSyntaxError)
from django.utils import timezone
from cms_contexts.decorators import detect_language
from cms_contexts.utils import handle_faulty_templates

from cms.models import PageMenu


logger = logging.getLogger(__name__)
register = template.Library()


@detect_language
@register.simple_tag(takes_context=True)
def load_menu(context, section, template):
    request = context['request']
    page_menu = PageMenu.objects.filter(section=section,
                                        menu__is_active=True,
                                        page__webpath=context['webpath']).first()
    if not page_menu: return ''
    language = request.LANGUAGE_CODE
    menu_items = page_menu.menu.get_localized_items(lang=language, 
                                                    parent__isnull=True)
    data = {'menu': menu_items}
    return handle_faulty_templates(template, data, name='load_menu')
