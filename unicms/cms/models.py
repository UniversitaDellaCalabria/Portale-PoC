import logging

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from cms_context.models import *
from taggit.managers import TaggableManager
from tinymce import models as tinymce_models

from . settings import *
from . utils import remove_file


logger = logging.getLogger(__name__)
CMS_IMAGE_CATEGORY_SIZE = getattr(settings, 'CMS_IMAGE_CATEGORY_SIZE',
                                  CMS_IMAGE_CATEGORY_SIZE)
CMS_BLOCK_SCHEMAS = getattr(settings, 'CMS_BLOCK_SCHEMAS',
                            CMS_BLOCK_SCHEMAS)
CMS_TEMPLATE_BLOCK_SECTIONS = getattr(settings, 'CMS_TEMPLATE_BLOCK_SECTIONS',
                                      CMS_TEMPLATE_BLOCK_SECTIONS)
PAGE_STATES = (('draft', _('Draft')),
               ('wait', _('Wait for a revision')),
               ('published', _('Published')),)


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


class SortableModel(models.Model):
    order = models.IntegerField(null=True, blank=True, default=10)

    class Meta:
        abstract = True
        ordering = ['order']


class ActivableModel(models.Model):
    is_active    = models.BooleanField()

    class Meta:
        abstract = True


class AbstractContextPublication(TimeStampedModel, ActivableModel):
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
    category          = models.ManyToManyField('Category')
    
    note              = models.TextField(null=True,blank=True,
                                         help_text=_('Editorial Board notes'))

    class Meta:
        abstract = True
        indexes = [
           models.Index(fields=['title']),
        ]


class AbstractPageBlock(TimeStampedModel, SortableModel, ActivableModel):
    name = models.CharField(max_length=60, blank=True, null=True,
                            help_text=_("Specify the container "
                                        "section in the template where "
                                        "this block would be rendered."))
    schema = models.TextField(choices=CMS_BLOCK_SCHEMAS,
                              blank=False, null=False)
    content = models.TextField(help_text=_("according to the "
                                           "block template schema"),
                               blank=True, null=True)
    section = models.CharField(max_length=60, blank=True, null=True,
                               help_text=_("Specify the container "
                                           "section in the template where "
                                           "this block would be rendered."),
                               choices=CMS_TEMPLATE_BLOCK_SECTIONS)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name        = models.CharField(max_length=160, blank=False,
                                   null=False, unique=False)
    description = models.TextField(max_length=1024,
                                   null=False, blank=False)
    image       = models.ImageField(upload_to="images/categories",
                                    null=True, blank=True,
                                    max_length=512)

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Content Categories")

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        remove_file(self.image.url)
        super(self.cls, self).delete(*args, **kwargs)

    def image_as_html(self):
        res = ""
        try:
            res = f'<img width={CMS_IMAGE_CATEGORY_SIZE} src="{self.image.url}"/>'
        except ValueError as e:
            # *** ValueError: The 'image' attribute has no file associated with it.
            res = f"{settings.STATIC_URL}images/no-image.jpg"
        return mark_safe(res)

    image_as_html.short_description = _('Image of this Category')
    image_as_html.allow_tags = True


# class SubCategory(TimeStampedModel):
    # name = models.CharField(max_length=160,
                            # blank=False, null=False, unique=False)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 # null=False, blank=False)
    # description  = models.TextField(null=False, blank=False)

    # class Meta:
        # ordering = ['name']
        # verbose_name_plural = _("SubCategory")

    # def __str__(self):
        # return '({}) {}'.format(self.category, self.name)


class PageTemplate(TimeStampedModel, ActivableModel):
    name = models.CharField(max_length=160,
                            blank=True, null=True)
    template_file = models.CharField(max_length=1024,
                                     blank=False, null=False,
                                     choices=CMS_PAGE_TEMPLATES)
    note = models.TextField(null=True, blank=True,
                            help_text=_("Editorial Board Notes, "
                                        "not visible by public."))

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Page Templates")

    def __str__(self):
        return '{} ({})'.format(self.name, self.template_file)


class PageTemplateThirdPartyBlock(TimeStampedModel, SortableModel, ActivableModel):
    template = models.ForeignKey(PageTemplate,
                                 on_delete=models.CASCADE,
                                 limit_choices_to={'is_active': True},)
    block = models.ForeignKey('PageBlock', null=False, blank=False,
                             on_delete=models.CASCADE)
    section = models.CharField(max_length=33, blank=True, null=True,
                               help_text=_("Specify the container "
                                           "section in the template where "
                                           "this block would be rendered."),
                               choices=CMS_TEMPLATE_BLOCK_SECTIONS)

    class Meta:
        verbose_name_plural = _("Page Template Third-Party Blocks")

    def __str__(self):
        return '({}) {} {}:{}'.format(self.template, self.block,
                                      self.order or '#',
                                      self.section or '#')


class PageBlockTemplate(AbstractPageBlock):
    template = models.ForeignKey(PageTemplate,
                                 null=False, blank=False,
                                 on_delete=models.CASCADE)
    template_file = models.CharField(max_length=1024,
                                     blank=False, null=False,
                                     choices=CMS_BLOCK_TEMPLATES,
                                     default='base.html')
    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Page Block HTML Templates")

    def __str__(self):
        return self.name if self.name else self.path


class ContextNavBarItem(TimeStampedModel, SortableModel, ActivableModel):
    """
    elements that builds up the navigation menu
    """
    context = models.ForeignKey(EditorialBoardContext,
                                on_delete=models.CASCADE,
                                limit_choices_to={'is_active': True},)
    name = models.CharField(max_length=33, blank=False, null=False)
    parent = models.ForeignKey('ContextNavBarItem',
                               null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name="related_page")
    url = models.URLField(help_text=_("url"), null=True, blank=True)
    page = models.ForeignKey('Page', null=True, blank=True,
                             on_delete=models.CASCADE)
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


class Page(TimeStampedModel, ActivableModel):
    name = models.CharField(max_length=160,
                            blank=False, null=False)
    context = models.ForeignKey(EditorialBoardContext,
                                on_delete=models.CASCADE,
                                limit_choices_to={'is_active': True},)
    base_template = models.ForeignKey(PageTemplate,
                                      on_delete=models.CASCADE,
                                      limit_choices_to={'is_active': True},)
    note = models.TextField(null=True, blank=True,
                            help_text=_("Editorial Board Notes, "
                                        "not visible by public."))

    date_start = models.DateTimeField()
    date_end = models.DateTimeField(null=True, blank=True)
    state = models.CharField(choices=PAGE_STATES, max_length=33,
                             default='draft')

    created_by = models.ForeignKey(get_user_model(),
                                   null=True, blank=True,
                                   on_delete=models.CASCADE,
                                   related_name='created_by')
    modified_by = models.ForeignKey(get_user_model(),
                                    null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='modified_by')
    
    category          = models.ManyToManyField('Category')
    tags = TaggableManager()

    def delete(self, *args, **kwargs):
        PageRelated.objects.filter(related_page=self).delete()
        super(Page, self).delete(*args, **kwargs)


    def save(self, *args, **kwargs):
        super(Page, self).save(*args, **kwargs)
        for rel in PageRelated.objects.filter(page=self):
            if not PageRelated.objects.\
                    filter(page=rel.related_page, related_page=self):
                PageRelated.objects.\
                    create(page=rel.page, related_page=self,
                           is_active=True)

    class Meta:
        verbose_name_plural = _("Pages")

    def get_category_img(self):
        return [i.image_as_html() for i in self.category.all()]

    def __str__(self):
        return '{} {}'.format(self.name, self.state)


class PageBlock(AbstractPageBlock):
    page = models.ForeignKey(Page, null=False, blank=False,
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = _("Page Block")

    def __str__(self):
        return '{} {} {}:{}'.format(self.page,
                                    self.order or '#',
                                    self.section or '#')


class PageThirdPartyBlock(TimeStampedModel, SortableModel, ActivableModel):
    page = models.ForeignKey(Page, null=False, blank=False,
                             on_delete=models.CASCADE)
    block = models.ForeignKey(PageBlock, null=False, blank=False,
                             on_delete=models.CASCADE)
    section = models.CharField(max_length=60, blank=True, null=True,
                               help_text=_("Specify the container "
                                           "section in the template where "
                                           "this block will be rendered."),
                               choices=CMS_TEMPLATE_BLOCK_SECTIONS)

    class Meta:
        verbose_name_plural = _("Page Third-Party Block")

    def __str__(self):
        return '{} {} {}:{}'.format(self.page, self.block,
                                    self.order or '#',
                                    self.section or '#')

class PageRelated(TimeStampedModel, SortableModel, ActivableModel):
    page = models.ForeignKey(Page, null=False, blank=False,
                             related_name='parent_page',
                             on_delete=models.CASCADE)
    related_page = models.ForeignKey(Page, null=False, blank=False,
                                     on_delete=models.CASCADE,
                                     related_name="related_page")

    class Meta:
        verbose_name_plural = _("Related Pages")
        unique_together = ("page", "related_page")

    def __str__(self):
        return '{} {}'.format(self.page, self.related_page)


class PageLink(TimeStampedModel):
    page = models.ForeignKey(Page, null=False, blank=False,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=False, blank=False)
    url = models.URLField(help_text=_("url"))

    class Meta:
        verbose_name_plural = _("Page Links")

    def __str__(self):
        return '{} {}' % (self.page, self.block_template)


class ContextPublication(AbstractContextPublication):
    context           = models.ManyToManyField(EditorialBoardContext,
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
        verbose_name_plural = _("Context Pubblications")

    def __str__(self):
        return '{} {}' % (self.context, self.title)


class ContextPublicationRelated(TimeStampedModel, SortableModel, ActivableModel):
    publication = models.ForeignKey(ContextPublication, null=False, blank=False,
                             related_name='parent_page',
                             on_delete=models.CASCADE)
    related = models.ForeignKey(ContextPublication, null=False, blank=False,
                                on_delete=models.CASCADE,
                                related_name="related_page")

    class Meta:
        verbose_name_plural = _("Related Publications")
        unique_together = ("publication", "related")

    def __str__(self):
        return '{} {}'.format(self.publication, self.related)


class ContextPublicationAttachment(TimeStampedModel, SortableModel, ActivableModel):
    publication = models.ForeignKey(ContextPublication, null=False, blank=False,
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


class ContextPublicationLocalization(TimeStampedModel, ActivableModel):
    context_publication = models.ForeignKey(ContextPublication, 
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
        verbose_name_plural = _("Context Publication Localizations")

    def __str__(self):
        return '{} {}'.format(self.context, self.language)


class ContextMediaCollection(TimeStampedModel):
    name        = models.CharField(max_length=160, blank=False,
                                   null=False, unique=False)
    description = models.TextField(max_length=1024,
                                   null=False, blank=False)

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Context Media Collections")

    def __str__(self):
        return self.name


class ContextMedia(TimeStampedModel):
    context = models.ForeignKey(EditorialBoardContext,
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
    
    collections = models.ManyToManyField('ContextMediaCollection')
    
    created_by = models.ForeignKey(get_user_model(),
                                   null=True, blank=True,
                                   on_delete=models.CASCADE,
                                   related_name='media_created_by')
    modified_by = models.ForeignKey(get_user_model(),
                                    null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='media_modified_by')
    
    class Meta:
        verbose_name_plural = _("Context Media")

    def __str__(self):
        return '{} {}' % (self.context, self.name)
