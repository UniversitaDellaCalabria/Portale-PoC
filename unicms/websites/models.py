from django.db import models
from django.utils.translation import gettext_lazy as _


class WebSite(models.Model):
    name = models.CharField(max_length=254, blank=False, null=False)
    domain = models.CharField(max_length=254, blank=False, null=False)
    is_active   = models.BooleanField()
    
    class Meta:
        verbose_name_plural = _("Sites")

    def __str__(self):
        return self.domain
