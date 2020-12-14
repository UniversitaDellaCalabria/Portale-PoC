import logging

from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.module_loading import import_string
from django.utils.safestring import SafeString

from cms.contexts.decorators import detect_language
from cms.contexts.utils import handle_faulty_templates
from cms.pages.models import Category
from cms.publications.models import PublicationContext


from cms.templates.settings import CMS_TEMPLATE_BLOCK_SECTIONS


logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(takes_context=True)
def blocks_in_position(context, position=None):
    request = context['request']
    page = context['page']
    webpath = context['webpath']

    positions_dict = dict(CMS_TEMPLATE_BLOCK_SECTIONS)
    if type(positions_dict[position] == dict):
        sub_positions = positions_dict[position]
        for item in sub_positions:
            page_blocks = page.get_blocks(section=item[0])
            for block in page_blocks:
                obj = import_string(block.type)(content=block.content,
                                                request=request,
                                                page=page,
                                                webpath=webpath)
                if obj: return True
    else:
        page_blocks = page.get_blocks(section=position)
        for block in page_blocks:
            obj = import_string(block.type)(content=block.content,
                                            request=request,
                                            page=page,
                                            webpath=webpath)
            if obj: return True
    return False
