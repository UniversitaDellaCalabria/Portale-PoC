import re 

from django.conf import settings
from django.http import (HttpResponse,
                         Http404,
                         HttpResponseBadRequest,
                         HttpResponseRedirect)
from django.shortcuts import render, get_object_or_404
from django.template import Template, Context
from django.template.loader import get_template, render_to_string
from django.utils.translation import gettext_lazy as _

from cms_contexts.handlers import BaseContentHandler
from cms_contexts.models import WebPath
from cms_contexts.utils import contextualize_template

from . models import PublicationContext, Category, Page
from . settings import *


class PublicationViewHandler(BaseContentHandler):
    template = "publication_view.html"
    
    def __init__(self, **kwargs):
        super(PublicationViewHandler, self).__init__(**kwargs)
        self.match_dict = self.match.groupdict()
        self.pub_context = PublicationContext.objects.filter(
                            is_active = True,
                            webpath__site=self.website,
                            webpath__fullpath=self.match_dict.get('webpath', '/'),
                            publication__slug=self.match_dict.get('slug', '')).first()
        self.page = Page.objects.filter(is_active=True,
                                   webpath=self.pub_context.webpath).first()
        self.webpath = self.pub_context.webpath
    
    def as_view(self):
        data = {'request': self.request,
                'webpath': self.pub_context.webpath,
                'website': self.website,
                'page': self.page,
                'path': self.match_dict.get('webpath', '/'),
                'publication_context': self.pub_context,
                'handler': self}
        
        ext_template_sources = contextualize_template(self.template, 
                                                      self.page)
        template = Template(ext_template_sources)
        context = Context(data)
        return HttpResponse(template.render(context), status=200)
   
    @property
    def parent_path_prefix(self):
        return getattr(settings, 'CMS_PUBLICATION_LIST_PREFIX_PATH',
                                  CMS_PUBLICATION_LIST_PREFIX_PATH)
    
    @property
    def parent_url(self):
        url = f'{self.webpath.fullpath}/{self.parent_path_prefix}/'
        return url.replace('//', '/')
    
    @property
    def breadcrumbs(self):
        leaf = (self.pub_context.url, getattr(self.pub_context.publication, 'title'))
        parent = (self.parent_url, _('News'))
        return (parent, leaf)


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
