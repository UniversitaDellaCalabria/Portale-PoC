import re 

from django.http import (HttpResponse,
                         Http404,
                         HttpResponseBadRequest,
                         HttpResponseRedirect)
from django.shortcuts import render, get_object_or_404
from django.template import Template, Context
from django.template.loader import get_template, render_to_string
from django.utils.translation import gettext_lazy as _

from cms_context.handlers import BaseContentHandler
from cms_context.models import WebPath
from cms_context.utils import contextualize_template

from . models import PublicationContext, Category, Page


class PublicationViewHandler(BaseContentHandler):
    template = "publication_view.html"

    def as_view(self):
        match_dict = self.match.groupdict()
        pub_context = PublicationContext.objects.filter(
                        is_active = True,
                        webpath__site=self.website,
                        webpath__fullpath=match_dict.get('webpath', '/'),
                        publication__slug=match_dict.get('slug', '')).first()
        page = Page.objects.filter(is_active=True,
                                   webpath=pub_context.webpath).first()
        data = {'request': self.request,
                'webpath': pub_context.webpath,
                'website': self.website,
                'page': page,
                'path': match_dict.get('webpath', '/'),
                'publication_context': pub_context}
        
        ext_template_sources = contextualize_template(self.template, page)
        template = Template(ext_template_sources)
        context = Context(data)
        return HttpResponse(template.render(context), status=200)


class PublicationListHandler(BaseContentHandler):
    template = "publication_list.html"

    @property
    def breadcrumbs(self):
        leaf = (self.path, _('News'))
        return (leaf,)
    
    def as_view(self):
        match_dict = self.match.groupdict()
        page = Page.objects.filter(is_active=True,
                                   webpath__site=self.website,
                                   webpath__fullpath=match_dict.get('webpath', '/'),).first()
        data = {'request': self.request,
                'webpath': page.webpath,
                'website': self.website,
                'page': page,
                'path': match_dict.get('webpath', '/'),
                'handler': self,
                }
        
        ext_template_sources = contextualize_template(self.template, page)
        template = Template(ext_template_sources)
        context = Context(data)
        return HttpResponse(template.render(context), status=200)
