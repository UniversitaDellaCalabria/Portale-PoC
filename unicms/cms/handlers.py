from django.template import Template, Context
from django.template.loader import get_template, render_to_string

from cms_context.handlers import BaseContentHandler
from cms_context.models import WebPath

from . models import Publication, Category


# https://docs.djangoproject.com/en/3.1/ref/templates/api/#loader-methods
class ContentViewHandler(BaseContentHandler):
    template = "publication_view.html"

    def match(self):
        WebPath ...

    def render(self):
        template = Template(self.template.template.source)
        context = Context({'request': self.request})
        return template.render(context)



class ContentListHandler(BaseContentHandler):
    template = "publication_list.html"
