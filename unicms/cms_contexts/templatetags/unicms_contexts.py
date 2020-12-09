import logging
import urllib

from django import template
from django.conf import settings
from django.template.loader import get_template, render_to_string
from django.template.exceptions import (TemplateDoesNotExist,
                                        TemplateSyntaxError)
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from cms_contexts.models import WebPath, WebSite
from cms_contexts.utils import handle_faulty_templates, sanitize_path
# WARNING - import circolare - decidere di migrare blocchi e menu in cms_pages
from cms_menus.models import NavigationBarItem

logger = logging.getLogger(__name__)
register = template.Library()


def _build_breadcrumbs(context):
    webpath = context['path']
    nodes = webpath.split('/')
    if nodes[-1] == '':
        del nodes[-1]

    crumbs = []
    root = '/'
    root_prefixed = f'/{settings.CMS_PATH_PREFIX}'

    for i in nodes:
        url = sanitize_path(f'{root}/{i}')
        url_prefixed = sanitize_path(f'{root_prefixed}/{i}')
        node_webpath = WebPath.objects.filter(fullpath=f'{url}/').first()
        node_name = node_webpath.name if node_webpath else i
        crumbs.append((url_prefixed, node_name))
        root = url
    crumbs[0] = [root_prefixed, _('Home')]
    return crumbs


@register.simple_tag(takes_context=True)
def language_menu(context, template=None, leaf=None):
    request = context['request']
    languages = {k:v for k,v in dict(settings.LANGUAGES).items()}
    current_args = urllib.parse.urlencode(request.GET)
    data = {v:f'?{current_args}&lang={k}' for k,v in languages.items()}
    if template:
        return handle_faulty_templates(template, data, name='language_menu')
    return data


@register.simple_tag(takes_context=True)
def breadcrumbs(context, template=None, leaf=None):
    template = template or 'breadcrumbs.html'
    crumbs = _build_breadcrumbs(context)
    if leaf:
        for i in leaf.breadcrumbs:
            crumbs.append(i)
    data = {'breadcrumbs': crumbs}
    return handle_faulty_templates(template, data, name='breadcrumbs')


@register.simple_tag(takes_context=True)
def call(context, obj, method, **kwargs):
    return getattr(obj, method)(**kwargs)


@register.simple_tag
def cms_sites():
    return WebSite.objects.filter(is_active=True).values_list('name', 'domain')
