import json

from django.utils.safestring import make_safe


class AbstractBlock(object):
    abtract = True
    
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)
        
    def render(self):
        return mark_safe(self.content)


class HtmlBlock(AbstractBlock):
    def __init__(self, content=''):
        self.content = content


class JSONBlock(AbstractBlock):
    def __init__(self, content=''):
        self.content = json.loads(content)
    
