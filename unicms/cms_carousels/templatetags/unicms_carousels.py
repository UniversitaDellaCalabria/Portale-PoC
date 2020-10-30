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
    carousel_items = carousel.carouselitem_set.filter(carousel=carousel,
                                                       is_active=True,).\
                                                       order_by('order')
    # i18n override
    language = request.LANGUAGE_CODE
    for i in carousel_items:
        i18n = i.carouselitemlocalization_set.filter(language=language).first()
        if i18n:
            i.heading = i18n.heading
            i.pre_heading = i18n.pre_heading
            i.description = i18n.description
    #
    data = {'carousel_items': carousel_items}
    return handle_faulty_templates(template, data, name='load_carousel')
