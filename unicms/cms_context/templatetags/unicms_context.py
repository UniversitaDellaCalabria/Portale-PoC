import logging

from django import template
from django.conf import settings
from django.template.loader import get_template, render_to_string
from django.template.exceptions import (TemplateDoesNotExist,
                                        TemplateSyntaxError)
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from cms_context.utils import handle_faulty_templates
# WARNING - import circolare - decidere di migrare blocchi e menu in cms_pages
from cms_menus.models import NavigationBarItem
from cms.views import detect_user_language

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(takes_context=True)
def breadcrumbs(context, template=None, leaf=None):
    template = template or 'breadcrumbs.html'
    nodes = context['context'].split()
    crumbs = []
    root = '/'
    for i in nodes:
        url = f'{root}/{i}'
        crumbs.append((url, i))
        root = url
    crumbs[0] = ('/', _('Home'))
    if leaf:
        crumbs.append((leaf.url, getattr(leaf, 'name', _('Here'))))
    data = {'breadcrumbs': crumbs}
    return handle_faulty_templates(template, data, name='breadcrumbs')
    
