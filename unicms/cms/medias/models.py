import logging

from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from cms.contexts.models import CreatedModifiedBy
from cms.contexts.models import WebPath
from cms.templates.models import (ActivableModel,
                                  SortableModel,
                                  TimeStampedModel)

from taggit.managers import TaggableManager

from . settings import *

logger = logging.getLogger(__name__)
FILETYPE_ALLOWED = getattr(settings, 'FILETYPE_ALLOWED',
                           FILETYPE_ALLOWED)


def context_media_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<year>/<filename>
    return 'medias/{}/{}'.format(timezone.now().year,
                                 filename)

class AbstractMedia(models.Model):
    file_size = models.IntegerField(blank=True, null=True)
    file_type = models.CharField(choices=((i,i) for i in FILETYPE_ALLOWED),
                                   max_length=256,
                                   blank=True, null=True)

    @property
    def file_size_kb(self):
        if isinstance(self.file_size, int):
            return round(self.file_size / 1024)
   
    @property
    def file_size_mb(self):
        if isinstance(self.file_size, int):
            return round(self.file_size_kb / 1024)
    
    class Meta:
        abstract = True


class MediaCollection(ActivableModel, TimeStampedModel, 
                      CreatedModifiedBy):
    name = models.CharField(max_length=160, blank=False,
                            null=False, unique=False)
    description = models.TextField(max_length=1024,
                                   null=False, blank=False)
    tags = TaggableManager()

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Media Collections")
        
    def __str__(self):
        return self.name


class Media(ActivableModel, TimeStampedModel, AbstractMedia, 
            CreatedModifiedBy):
    title = models.CharField(max_length=60, blank=True, null=True,
                             help_text=_("Media file title"))
    file = models.FileField(upload_to=context_media_path)
    description = models.TextField()

    class Meta:
        verbose_name_plural = _("Media")

    def get_media_path(self):
        return f'{settings.MEDIA_URL}{self.file}'

    def __str__(self):
        return '{} {}'.format(self.title, self.file_type)


class MediaCollectionItem(ActivableModel, SortableModel, 
                          TimeStampedModel, CreatedModifiedBy):
    media = models.ForeignKey(Media, on_delete=models.CASCADE,
                              limit_choices_to={'is_active': True},)
    collection = models.ForeignKey(MediaCollection,
                                   on_delete=models.CASCADE,
                                   limit_choices_to={'is_active': True},)

    class Meta:
        ordering = ['order']
        verbose_name_plural = _("Media Collection Items")

    def __str__(self):
        return '{} {}'.format(self.collection, self.media)
