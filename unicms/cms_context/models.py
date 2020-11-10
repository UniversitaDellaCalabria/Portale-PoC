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
    parent = models.ForeignKey('WebPath',
                               null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name="related_path",
                               help_text=_('path be prefixed with '
                                           'the parent one, on save'))
    path = models.TextField(max_length=2048, null=False, blank=False)
    fullpath = models.TextField(max_length=2048, null=True, blank=True,
                                help_text=_("final path prefixed with the "
                                            "parent path"))
    is_active   = models.BooleanField()

    class Meta:
        verbose_name_plural = _("Site Contexts (WebPaths)")

    def split(self) -> list:
        """
        return splitted nodes in a list
        """
        if self.path == '/':
            return ['/']
        return self.path.split('/')

    def save(self, *args, **kwargs):
        if self.parent:
            # update fullpath
            fullpath = f'{self.parent.path}/{self.path}'.replace('//', '/')
            if fullpath != self.fullpath: 
                self.fullpath = fullpath
            
            return super(WebPath, self).save(*args, **kwargs)
            
            # update also its childs
            for child_path in WebPath.objects.filter(parent=self):
                child_path.save()
        else:
            self.fullpath = self.path
            return super(WebPath, self).save(*args, **kwargs)
        
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
        verbose_name_plural = _("Editorial Board Users")

    def __str__(self):
        if getattr(self, 'context'):
            return '{} {} in {}'.format(self.user, self.permission, self.context)
        else:
            return '{} {}'.format(self.user, self.permission)
