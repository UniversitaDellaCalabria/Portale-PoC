import logging

from django import template
from django.conf import settings
from django.template.loader import get_template, render_to_string
from django.template.exceptions import (TemplateDoesNotExist,
                                        TemplateSyntaxError)
from django.utils import timezone
from django.utils.safestring import mark_safe
# WARNING - import circolare - decidere di migrare blocchi e menu in cms_pages
from cms_menus.models import NavigationBarItem
from cms.views import detect_user_language

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def supported_languages():
    return settings.LANGUAGES


# @register.simple_tag(takes_context=True)
# def load_blocks(context, template):
    # t = get_template(template)
