import logging
import re

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import (HttpResponse,
                         Http404,
                         HttpResponseBadRequest,
                         HttpResponseRedirect)
from django.shortcuts import render, get_object_or_404
from django.utils.module_loading import import_string

from cms_context.decorators import detect_language
from cms_context.models import WebSite, WebPath
from cms_context.utils import detect_user_language
from urllib.parse import urlparse
from . models import Page

logger = logging.getLogger(__name__)


@detect_language
def cms_content(request):
    requested_site = re.match('^[a-zA-Z0-9\.\-\_]*',
                              # request.headers.get('Host', '')
                              request.get_host()).group()
    website = get_object_or_404(WebSite, domain = requested_site)

    if not website:
        return HttpResponseBadRequest()

    path = urlparse(request.get_full_path()).path

    # detect if webpath is referred to a specialized app
    for k,v in settings.CMS_APP_REGEXP_URLPATHS.items():
        logger.debug('APP REGEXP URL HANDLERS: {}: {}'.format(k, v))
        match = re.match(v, path)
        if not match:
            continue
        query = match.groupdict()
        params = {'request': request,
                  'website': website,
                  'path': path,
                  'match': match}
        params.update(query)
        handler = import_string(k)(**params)
        return handler.as_view()

    # go further with webpath matching
    context = get_object_or_404(WebPath, fullpath=path, site=website)
    page = Page.objects.filter(context = context,
                               is_active = True,
                               state = 'published').first()
    if not page:
        raise Http404()

    context_vars = {
        'website': website,
        'path': path,
        'context': context,
        'page': page,
    }
    return render(request,
                  page.base_template.template_file, context_vars)
