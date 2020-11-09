from django.template import Template

from . models import WebPath


class BaseContentHandler(object):
    
    def __init__(self, context:WebPath, template_fname:str, path:str):
        """
            Checks if a path belongs to a CMS specialized application
            :type context: cms_context.model.WebPath
            :type template_fname: String to be opened as file.
                                  its content would be the Template() object
                                  string argument
                                  
                                  template = Template(open(template_fname).read())
                                  context = Context({"my_name": "Adrian"})
                                  template.render(context)
            :type path: String
            :param context: the context where it should belong to. 
                            Its fullpath should be a kind of prefix of 
                            settings.CMS_PUBLICATION_URLPATH_REGEXP
            :param template: 
            :param path: 
            :return: render the HTML page
        """
        raise NotImplementedError()
    
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
        
    def render(self):
        """
            get the template configured for this resources (self.template)
            open 
            returns a rendered page
        """
        raise NotImplementedError()
