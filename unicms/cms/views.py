import re

from django.contrib.sites.shortcuts import get_current_site
from django.http import (HttpResponse,
                         Http404,
                         HttpResponseBadRequest,
                         HttpResponseRedirect)
from django.shortcuts import render, get_object_or_404
from django.utils import translation

from cms_context.models import WebSite, WebPath
from . models import Page


def get_request_lang(request):
    lang = request.GET.get('lang',
                           translation.get_language_from_request(request))
    return lang


def cms_content(request):
    requested_site = re.match('^[a-zA-Z0-9\.\-\_]*',
                              # request.headers.get('Host', '')
                              request.get_host()).group()
    website = get_object_or_404(WebSite, domain = requested_site)

    if not website:
        return HttpResponseBadRequest()

    path = request.get_full_path()
    context = get_object_or_404(WebPath, path=path, site=website)
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
    return render(request, page.base_template.template_file, context_vars)
