from django.conf import settings
from django.template import Template
from django.template.loader import get_template

from . models import WebPath


class BaseContentHandler(object):
    template = "default_template.html"
    
    def __init__(self, context:WebPath, path:str, 
                 template_fname:str = None):
        """
        Checks if a path belongs to a CMS specialized application
        :type context: cms_context.model.WebPath
        :type path: String
        :type template_fname: String.            
        :param context: the context where it should belong to. 
                        Its fullpath should be a kind of prefix of 
                        settings.CMS_PUBLICATION_URLPATH_REGEXP
        :param path: 
        :param template: If present override the default one.
                         its content would be the Template() object
                         string argument
                        
                         template = Template(open(template_fname).read())
                         context = Context({"my_name": "Adrian"})
                         template.render(context)
        :return: render the HTML page
        """
        self.context = context
        self.path = path
        self.template = get_template(template_fname) \
                        if template_fname else get_template(template)
        
    
    def match -> bool(self):
        """
        check if settings.CMS_PUBLICATION_URLPATH_REGEXP matches
        with the given path. Return True or False
        """
        raise NotImplementedError()
    
    def get(self):
        """
            returns a queryset with the results
        """
        raise NotImplementedError()

    def url(self):
        """
            returns an absolute url to the render view
        """
        raise NotImplementedError()

    def render(self):
        """
            get the template configured for this resources (self.template)
            open 
            returns a rendered page
        """
        raise NotImplementedError()