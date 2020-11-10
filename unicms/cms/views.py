import re

from django.contrib.sites.shortcuts import get_current_site
from django.http import (HttpResponse,
                         Http404,
                         HttpResponseBadRequest,
                         HttpResponseRedirect)
from django.shortcuts import render, get_object_or_404

from cms_context.decorators import detect_language
from cms_context.models import WebSite, WebPath
from cms_context.utils import detect_user_language
from urllib.parse import urlparse
from . models import Page


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
