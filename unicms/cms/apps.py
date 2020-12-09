from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CmsConfig(AppConfig):
    name = 'cms'
    verbose_name = _('cms')

    def ready(self):
        # that actually loads the signals
        import cms.signals
