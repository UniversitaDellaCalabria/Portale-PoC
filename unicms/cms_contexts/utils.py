import logging
import re

from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe
from django.template.loader import get_template, render_to_string
from django.template.exceptions import (TemplateDoesNotExist,
                                        TemplateSyntaxError)


logger = logging.getLogger(__name__)
CMS_PATH_PREFIX = getattr(settings, 'CMS_PATH_PREFIX', '')


def detect_user_language(request):
    lang = request.GET.get('lang',
                           translation.get_language_from_request(request))
    translation.activate(lang)
    request.LANGUAGE_CODE = translation.get_language()
    return lang


def handle_faulty_templates(template: str, data: dict, name='', ):
    _error_msg = 'ERROR: {} template tags: {}'
    _error_msg_pub = '<!-- Error {} template tags. See log file. -->'
    
    try:
        return render_to_string(template, data)
    except TemplateDoesNotExist as e:
        logger.error(_error_msg.format(name, e))
    except TemplateSyntaxError as e:
        logger.error(_error_msg.format(name, e))

    return mark_safe(_error_msg_pub)


def build_breadcrumbs(context):
    webpath = context['webpath']
    nodes = webpath.split()
    crumbs = []
    root = '/' 
    for i in nodes:
        url = f'{root}/{i}'
        crumbs.append((url, i))
        root = url
    crumbs[0] = (f'/{CMS_PATH_PREFIX}', webpath.name) 
    return crumbs


def contextualize_template(template_fname, page):
    template_obj = get_template(template_fname)
    template_sources = template_obj.template.source

    # do additional preprocessing on the template here ...
    # get/extends the base template of the page context
    base_template_tag = f'{{% extends "{page.base_template.template_file}" %}}'
    regexp = "\{\%\s*extends\s*\t*[\'\"a-zA-Z0-9\_\-\.]*\s*\%\}"
    ext_template_sources = re.sub(regexp, base_template_tag, template_sources)
    # end string processing
    return ext_template_sources


def sanitize_path(path):
    return re.sub('/[/]+', '/', path)
