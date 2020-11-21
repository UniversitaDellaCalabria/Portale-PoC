from django.contrib.auth import get_user_model
from django.db import models


class AbstractPreviewable(models.Model):
    draft_of = models.IntegerField(null=True, blank=True)
    
    locked_by = models.ForeignKey(get_user_model(), null=True, blank=True)
    locked_time = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True

    
