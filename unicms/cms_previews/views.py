from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404

from cms_contexts.decorators import detect_language
from cms_contexts.models import WebPath
from cms_contexts.utils import detect_user_language
from urllib.parse import urlparse
from . models import Page


# @is_allowed
@detect_language
def preview(request, webpath_pk, app_label, model, pk):
    """
        `/cms_previews/<webpath_pk:id>/<app_label:str>/<model:str>/<pk:int>`
    """
    content_type = ContentType.objects.get(app_label=app_label, 
                                           model=model)
    content = content_type.get_object_for_this_type(pk=pk)

    webpath = get_object_or_404(WebPath, pk=webpath_pk)
    page = Page.objects.filter(webpath = webpath).first()
    if not page:
        raise Http404()

    context = {
        'website': website,
        'path': path,
        'webpath': webpath,
        'page': page,
    }
    return render(request, page.base_template.template_file, context)
