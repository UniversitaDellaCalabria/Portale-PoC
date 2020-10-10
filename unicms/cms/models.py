import logging

from django.contrib.auth import get_user_model
# from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from cms_context.models import *
from cms_pages.models import Category, PAGE_STATES
from cms_templates.models import (CMS_TEMPLATE_BLOCK_SECTIONS,
                                  ActivableModel, 
                                  SortableModel,
                                  TimeStampedModel)
                                  
from taggit.managers import TaggableManager
from tinymce import models as tinymce_models

from . settings import *
from . utils import remove_file


logger = logging.getLogger(__name__)


def context_publication_attachment_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{}/{}/{}/{}'.format(instance.context.site, 
                                instance.context.pk,
                                instance.pk,
                                filename)

def context_media_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{}/{}/{}'.format(instance.context.site, 
                                instance.context.pk,
                                filename)


class AbstractPublication(TimeStampedModel, ActivableModel):
    title             = models.CharField(max_length=256, 
                                       null=False, blank=False,
                                       help_text=_("Heading, Headline"))
    
    subheading        = models.TextField(max_length=1024, 
                                         null=True,blank=True, 
                                         help_text=_("Strap line (press)"))
    content           =  tinymce_models.HTMLField(null=True,blank=True,
                                                  help_text=_('Content'))
    state             = models.CharField(choices=PAGE_STATES, 
                                         max_length=33,
                                         default='draft')
    date_start        = models.DateTimeField(null=True,blank=True)
    date_end          = models.DateTimeField(null=True,blank=True)
    category          = models.ManyToManyField(Category)
    
    note              = models.TextField(null=True,blank=True,
                                         help_text=_('Editorial Board notes'))

    class Meta:
        abstract = True
        indexes = [
           models.Index(fields=['title']),
        ]


class NavigationBarItem(TimeStampedModel, SortableModel, ActivableModel):
    """
    elements that builds up the navigation menu
    """
    context = models.ForeignKey(WebPath,
                                on_delete=models.CASCADE,
                                limit_choices_to={'is_active': True},)
    name = models.CharField(max_length=33, blank=False, null=False)
    parent = models.ForeignKey('NavigationBarItem',
                               null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name="related_page")
    url = models.URLField(help_text=_("url"), null=True, blank=True)
    section = models.CharField(max_length=60, blank=True, null=True,
                               help_text=_("Specify the container "
                                           "section in the template where "
                                           "this menu will be rendered."),
                               choices=CMS_TEMPLATE_BLOCK_SECTIONS)
    
    class Meta:
        verbose_name_plural = _("Context Navigation Menu Items")

    def __str__(self):
        return '({}) {} {}'.format(self.context,
                                   self.name, self.parent or '')


class Publication(AbstractPublication):
    context           = models.ManyToManyField(WebPath,
                                               limit_choices_to={'is_active': True},)
    
    slug              = models.SlugField(null=True, blank=True)
    in_evidence_start = models.DateTimeField(null=True,blank=True)
    in_evidence_end   = models.DateTimeField(null=True,blank=True)
    tags = TaggableManager()
    
    created_by = models.ForeignKey(get_user_model(),
                                   null=True, blank=True,
                                   on_delete=models.CASCADE,
                                   related_name='pub_created_by')
    modified_by = models.ForeignKey(get_user_model(),
                                    null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='pub_modified_by')
    
    class Meta:
        verbose_name_plural = _("Publications")

    def __str__(self):
        return '{} {}' % (self.context, self.title)


class PublicationRelated(TimeStampedModel, SortableModel, ActivableModel):
    publication = models.ForeignKey(Publication, null=False, blank=False,
                             related_name='parent_page',
                             on_delete=models.CASCADE)
    related = models.ForeignKey(Publication, null=False, blank=False,
                                on_delete=models.CASCADE,
                                related_name="related_page")

    class Meta:
        verbose_name_plural = _("Related Publications")
        unique_together = ("publication", "related")

    def __str__(self):
        return '{} {}'.format(self.publication, self.related)


class PublicationAttachment(TimeStampedModel, SortableModel, ActivableModel):
    publication = models.ForeignKey(Publication, null=False, blank=False,
                                    related_name='page_attachment',
                                    on_delete=models.CASCADE)
    name = models.CharField(max_length=60, blank=True, null=True,
                    help_text=_("Specify the container "
                                "section in the template where "
                                "this block would be rendered."))
    file = models.FileField(upload_to=context_publication_attachment_path)
    description = models.TextField()
    
    file_size = models.IntegerField(blank=True, null=True)
    file_format = models.CharField(choices=((i,i) for i in FILETYPE_ALLOWED),
                                   max_length=256,
                                   blank=True, null=True)

    class Meta:
        verbose_name_plural = _("Publication Attachments")

    def __str__(self):
        return '{} {} ({})'.format(self.publication, self.name, 
                                   self.file_format)


class PublicationLocalization(TimeStampedModel, ActivableModel):
    context_publication = models.ForeignKey(Publication, 
                                            null=False, blank=False,
                                            on_delete=models.CASCADE)
    language   = models.CharField(choices=settings.LANGUAGES,
                                  max_length=12, null=False,blank=False,
                                  default='en')
    subheading        = models.TextField(max_length=1024, 
                                         null=True,blank=True, 
                                         help_text=_("Strap line (press)"))
    content           =  tinymce_models.HTMLField(null=True,blank=True,
                                                  help_text=_('Content'))
    created_by = models.ForeignKey(get_user_model(),
                                   null=True, blank=True,
                                   on_delete=models.CASCADE,
                                   related_name='publoc_created_by')
    modified_by = models.ForeignKey(get_user_model(),
                                    null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='publoc_modified_by')
    class Meta:
        verbose_name_plural = _("Publication Localizations")

    def __str__(self):
        return '{} {}'.format(self.context, self.language)


class MediaCollection(TimeStampedModel):
    name        = models.CharField(max_length=160, blank=False,
                                   null=False, unique=False)
    description = models.TextField(max_length=1024,
                                   null=False, blank=False)

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Media Collections")

    def __str__(self):
        return self.name


class Media(TimeStampedModel):
    context = models.ForeignKey(WebPath,
                                on_delete=models.CASCADE,
                                limit_choices_to={'is_active': True},)
    name = models.CharField(max_length=60, blank=True, null=True,
                        help_text=_("Specify the container "
                                    "section in the template where "
                                    "this block would be rendered."))
    file = models.FileField(upload_to=context_media_path)
    description = models.TextField()
    
    file_size = models.IntegerField(blank=True, null=True)
    file_format = models.CharField(choices=((i,i) for i in FILETYPE_ALLOWED),
                                   max_length=256,
                                   blank=True, null=True)
    
    collections = models.ManyToManyField('MediaCollection')
    
    created_by = models.ForeignKey(get_user_model(),
                                   null=True, blank=True,
                                   on_delete=models.CASCADE,
                                   related_name='media_created_by')
    modified_by = models.ForeignKey(get_user_model(),
                                    null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='media_modified_by')
    
    class Meta:
        verbose_name_plural = _("Media")

    def __str__(self):
        return '{} {}' % (self.context, self.name)
