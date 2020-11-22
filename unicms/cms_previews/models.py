from django.contrib.auth import get_user_model
from django.db import models


class AbstractDraftable(models.Model):
    draft_of = models.IntegerField(null=True, blank=True)
       
    class Meta:
        abstract = True
    
