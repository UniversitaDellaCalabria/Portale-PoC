from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _


class WebSite(Site):
    is_active   = models.BooleanField()
    
    class Meta:
        verbose_name_plural = _("Sites")

    def __str__(self):
        return self.domain
