import re 

from django.http import (HttpResponse,
                         Http404,
                         HttpResponseBadRequest,
                         HttpResponseRedirect)
from django.shortcuts import render, get_object_or_404
from django.template import Template, Context
from django.template.loader import get_template, render_to_string

from cms_context.handlers import BaseContentHandler
from cms_context.models import WebPath

from . models import PublicationContext, Category, Page


def contextualize_template(template_fname, page):
    template_obj = get_template(template_fname)
    template_sources = template_obj.template.source

    # do additional preprocessing on the template here ...
    # get/extends the base template of the page context
    base_template_tag = f'{{% extends "{page.base_template.template_file}" %}}'
    regexp = "\{\%\s*extends\s*\t*[\'\"a-zA-Z0-9\_\-\.]*\s*\%\}"
    ext_template_sources = re.sub(regexp, base_template_tag, template_sources)
    # end string processing
    return ext_template_sources


class PublicationViewHandler(BaseContentHandler):
    template = "publication_view.html"

    def as_view(self):
        match_dict = self.match.groupdict()
        pub_context = PublicationContext.objects.filter(
                        is_active = True,
                        context__site=self.website,
                        context__fullpath=match_dict.get('context', '/'),
                        publication__slug=match_dict.get('slug', '')).first()
        page = Page.objects.filter(is_active=True,
                                   context=pub_context.context).first()
        data = {'request': self.request,
                'context': pub_context.context,
                'website': self.website,
                'page': page,
                'path': match_dict.get('context', '/'),
                'publication_context': pub_context}
        
        ext_template_sources = contextualize_template(self.template, page)
        template = Template(ext_template_sources)
        context = Context(data)
        return HttpResponse(template.render(context), status=200)


class PublicationListHandler(BaseContentHandler):
    template = "publication_list.html"

    def as_view(self):
        match_dict = self.match.groupdict()
        page = Page.objects.filter(is_active=True,
                                   context__site=self.website,
                                   context__fullpath=match_dict.get('context', '/'),).first()
        data = {'request': self.request,
                'context': page.context,
                'website': self.website,
                'page': page,
                'path': match_dict.get('context', '/'),
                # 'publication_context': pub_context
                }
        
        ext_template_sources = contextualize_template(self.template, page)
        template = Template(ext_template_sources)
        context = Context(data)
        return HttpResponse(template.render(context), status=200)
