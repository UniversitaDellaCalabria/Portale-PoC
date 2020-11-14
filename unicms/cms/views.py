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
def cms_dispatch(request):
    requested_site = re.match('^[a-zA-Z0-9\.\-\_]*',
                              # request.headers.get('Host', '')
                              request.get_host()).group()
    website = get_object_or_404(WebSite, domain = requested_site)

    if not website:
        return HttpResponseBadRequest()

    path = urlparse(request.get_full_path()).path
    
    _msg_head = 'APP REGEXP URL HANDLERS:'
    # detect if webpath is referred to a specialized app
    for k,v in settings.CMS_APP_REGEXP_URLPATHS.items():
        logger.debug(f'{_msg_head} - {k}: {v}')
        match = re.match(v, path)
        if not match:
            logger.debug(f'{_msg_head} - {k}: {v} -> UNMATCH with {path}')
            continue
        # TODO: some more checks
        # elif len(match.groupdict()) > 1:
            # ## if something collides takes only the first for resielence
            # breakpoint()
            # query = dict(list(match.groupdict().items())[0])
            # logger.warning(f'{_msg_head} - Multiple regexp collision: {match}')
        else:
            query = match.groupdict()
        params = {'request': request,
                  'website': website,
                  'path': path,
                  'match': match}
        params.update(query)
        handler = import_string(k)(**params)
        try:
            return handler.as_view()
        except Exception as e:
            logger.exception(f'{path}:{e}')

    # go further with webpath matching
    webpath = get_object_or_404(WebPath, fullpath=path, site=website)
    page = Page.objects.filter(webpath = webpath,
                               is_active = True,
                               state = 'published').first()
    if not page:
        raise Http404()

    context = {
        'website': website,
        'path': path,
        'webpath': webpath,
        'page': page,
    }
    return render(request, page.base_template.template_file, context)
