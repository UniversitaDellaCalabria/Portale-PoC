from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404

from cms_context.decorators import detect_language
from cms_context.models import WebPath
from cms_context.utils import detect_user_language
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

    context = get_object_or_404(WebPath, pk=webpath_pk)
    page = Page.objects.filter(context = context).first()
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
