import logging

from django import template
from django.conf import settings
from django.utils import timezone
from django.utils.safestring import mark_safe

from cms.models import PageCarousel
from cms_context.decorators import detect_language
from cms_context.utils import handle_faulty_templates


logger = logging.getLogger(__name__)
register = template.Library()


@detect_language
@register.simple_tag(takes_context=True)
def load_carousel(context, section, template):
    request = context['request']
    
    page = PageCarousel.objects.filter(section=section,
                                       is_active=True,
                                       page__context=context['context']).first()
    if not page: return ''
    else: carousel = page.carousel    
    
    language = request.LANGUAGE_CODE
    carousel_items = carousel.get_localized_items(lang=language)
    data = {'carousel_items': carousel_items}
    return handle_faulty_templates(template, data, name='load_carousel')