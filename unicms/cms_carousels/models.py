from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from cms_context.models import WebPath
from cms_medias.models import Media
from cms_templates.models import (ActivableModel, 
                                  SortableModel,
                                  TimeStampedModel)


class Carousel(ActivableModel, TimeStampedModel):
    name        = models.CharField(max_length=160, blank=False,
                                   null=False, unique=False)
    description = models.TextField(max_length=2048,
                                   null=False, blank=False)

    created_by = models.ForeignKey(get_user_model(),
                                   null=True, blank=True,
                                   on_delete=models.CASCADE,
                                   related_name='carousel_created_by')
    modified_by = models.ForeignKey(get_user_model(),
                                    null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='carousel_modified_by')

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Carousels")

    def __str__(self):
        return self.name


class CarouselItem(ActivableModel, TimeStampedModel, SortableModel):
    carousel = models.ForeignKey(Carousel,
                                 on_delete=models.CASCADE)
    image = models.ForeignKey(Media, on_delete=models.CASCADE)
    pre_heading = models.CharField(max_length=120, blank=True, null=True,
                                   help_text=_("Pre Heading"))
    heading = models.CharField(max_length=120, blank=True, null=True,
                             help_text=_("Heading"))
    
    # hopefully markdown here!
    description = models.TextField()
    
    class Meta:
        verbose_name_plural = _("Carousel Items")

    def __str__(self):
        return '{} {}' % (self.carousel, self.heading)


class CarouselItemLink(ActivableModel, TimeStampedModel, SortableModel):
    carousel = models.ForeignKey(CarouselItem,
                                 on_delete=models.CASCADE)
    title = models.CharField(max_length=120, blank=True, null=True,
                             help_text=_("Title"))
    url = models.CharField(max_length=2048)
    
    class Meta:
        verbose_name_plural = _("Carousel Item Links")

    def __str__(self):
        return '{} {}' % (self.carousel, self.url)
