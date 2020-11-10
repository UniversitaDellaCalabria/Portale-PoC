from django.template import Template

from cms_content.handlers import BaseContentHandler
from cms_context.models import WebPath
from . models import Publication, Category


# https://docs.djangoproject.com/en/3.1/ref/templates/api/#loader-methods
class ContentListHandler(BaseContentHandler):
    template = "publication_list.html"


class ContentViewHandler(BaseContentHandler):
    template = "publication_view.html"
