from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CmsSearchConfig(AppConfig):
    name = 'cms_search'
    verbose_name = _('cms_searches')

    def ready(self):
        # that actually loads the signals
        import cms_search.signals
