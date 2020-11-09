from django.template import Template

from cms_content.handlers import BaseContentHandler
from cms_context.models import WebPath
from . models import Publication, Category


class ContentListHandler(BaseContentHandler):
    pass


class ContentViewHandler(BaseContentHandler):
    pass
