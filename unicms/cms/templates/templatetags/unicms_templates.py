import logging

from django import template
from django.conf import settings
from django.template.loader import get_template, render_to_string
from django.template.exceptions import (TemplateDoesNotExist,
                                        TemplateSyntaxError)
from django.utils import timezone
from django.utils.safestring import mark_safe


logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def supported_languages():
    return settings.LANGUAGES
