import logging

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

from cms_templates.models import TimeStampedModel

from . import settings as app_settings


logger = logging.getLogger(__name__)
CMS_CONTEXT_PERMISSIONS = getattr(settings, 'CMS_CONTEXT_PERMISSIONS',
                                  app_settings.CMS_CONTEXT_PERMISSIONS)

class WebSite(Site):
    is_active   = models.BooleanField()
    
    class Meta:
        verbose_name_plural = _("Sites")

    def __str__(self):
        return self.domain


class WebPath(TimeStampedModel):
    """
    A Page can belong to one or more Context
    A editor/moderator can belong to one or more Context
    The same for Page Templates
    """
    site = models.ForeignKey(WebSite, on_delete=models.CASCADE)
    name = models.CharField(max_length=254, blank=False, null=False)
    path = models.TextField(max_length=2048, null=False, blank=False)
    is_active   = models.BooleanField()

    class Meta:
        verbose_name_plural = _("Site Contexts")

    def __str__(self):
        return '{}: {} ({})'.format(self.site, self.name, self.path)


class EditorialBoardEditors(TimeStampedModel):
    """
    A Page can belong to one or more Context
    A editor/moderator can belong to one or more Context
    The same for Page Templates
    """
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE)
    permission = models.CharField(max_length=5, blank=False, null=False,
                                  choices=CMS_CONTEXT_PERMISSIONS)
    context = models.ForeignKey(WebPath,
                                on_delete=models.CASCADE,
                                null=True, blank=True)
    is_active   = models.BooleanField()

    class Meta:
        verbose_name_plural = _("Context Editors")

    def __str__(self):
        if getattr(self, 'context'):
            return '{} {} in {}'.format(self.user, self.permission, self.context)
        else:
            return '{} {}'.format(self.user, self.permission)
