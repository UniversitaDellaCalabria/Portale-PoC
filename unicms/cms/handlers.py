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
        template_obj = get_template(self.template)
        template_sources = template_obj.template.source

        # do additional preprocessing on the template here ...
        # ...
        # end string processing

        template = Template(template_sources)
        context = Context(data)
        return HttpResponse(template.render(context),
                            status=200)


class PublicationListHandler(BaseContentHandler):
    template = "publication_list.html"
