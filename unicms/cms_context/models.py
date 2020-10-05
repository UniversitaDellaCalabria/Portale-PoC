import logging

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _ 

from . import settings as app_settings

logger = logging.getLogger(__name__)


CMS_CONTEXT_PERMISSIONS = getattr(settings, 'CMS_CONTEXT_PERMISSIONS',
                                  app_settings.CMS_CONTEXT_PERMISSIONS)

class TimeStampedModel(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified =  models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True
 

class Site(TimeStampedModel):
    fqdn = models.CharField(max_length=160, blank=False, 
                            null=False, unique=True,
                            help_text=_('server FQDN'))
    is_active   = models.BooleanField()
    
    class Meta:
        verbose_name_plural = _("EditorialBoard Sites")
    
    def __str__(self):
        return self.fqdn


class EditorialBoardContext(TimeStampedModel):
    """
    A Page can belong to one or more Context
    A editor/moderator can belong to one or more Context
    The same for Page Templates
    """
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    name = models.CharField(max_length=254, blank=False, null=False)
    path = models.TextField(max_length=2048, null=False, blank=False)
    is_active   = models.BooleanField()
    
    class Meta:
        verbose_name_plural = _("EditorialBoard Site Contexts")
    
    def __str__(self):
        return '{}: {} ({})'.format(self.site, self.name, self.path)


class EditorialBoardRolePermissions(TimeStampedModel):
    name = models.CharField(max_length=160, blank=False, 
                            null=False, unique=True)
    permission = models.CharField(max_length=5, blank=False, 
                                  null=False, choices=CMS_CONTEXT_PERMISSIONS)
    is_active   = models.BooleanField()
    class Meta:
        ordering = ['name']
        verbose_name_plural = _("EditorialBoard Role Permissions")
    
    def __str__(self):
        return self.name


class EditorialBoardUsers(TimeStampedModel):
    """
    A Page can belong to one or more Context
    A editor/moderator can belong to one or more Context
    The same for Page Templates
    """
    user = models.ForeignKey(get_user_model(), 
                             on_delete=models.CASCADE)
    role = models.ForeignKey(EditorialBoardRolePermissions, on_delete=models.CASCADE)
    context = models.ForeignKey(EditorialBoardContext, 
                                on_delete=models.CASCADE,
                                null=True, blank=True)
    is_active   = models.BooleanField()
    
    class Meta:
        verbose_name_plural = _("EditorialBoard Context Users")
    
    def __str__(self):
        if getattr(self, 'context'):
            return '{} {} in {}'.format(self.user, self.role, self.context)
        else:
            return '{} {}'.format(self.user, self.role)
