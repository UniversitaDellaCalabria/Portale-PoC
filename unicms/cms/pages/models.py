import logging

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.module_loading import import_string
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from cms.contexts.models import *
from cms.contexts.utils import sanitize_path
from cms.carousels.models import Carousel
from cms.medias import settings as cms_media_settings
from cms.medias.models import Media, MediaCollection, AbstractMedia
from cms.menus.models import NavigationBar
from cms.templates.models import (CMS_TEMPLATE_BLOCK_SECTIONS,
                                  TemplateBlock,
                                  ActivableModel,
                                  PageTemplate,
                                  SectionAbstractModel,
                                  SortableModel,
                                  TimeStampedModel)

from taggit.managers import TaggableManager


from . settings import *
from . utils import remove_file, load_hooks


logger = logging.getLogger(__name__)
FILETYPE_ALLOWED = getattr(settings, 'FILETYPE_ALLOWED',
                           cms_media_settings.FILETYPE_ALLOWED)
PAGE_STATES = (('draft', _('Draft')),
               ('published', _('Published')),)
CMS_IMAGE_CATEGORY_SIZE = getattr(settings, 'CMS_IMAGE_CATEGORY_SIZE',
                                  CMS_IMAGE_CATEGORY_SIZE)
CMS_PATH_PREFIX = getattr(settings, 'CMS_PATH_PREFIX', '')


class AbstractDraftable(models.Model):
    draft_of = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class AbstractPublicable(models.Model):

    @property
    def is_publicable(self) -> bool:
        now = timezone.localtime()
        result = False
        if self.is_active and \
           self.state == 'published' and \
           self.date_start <= now :
            result = True
        if self.date_end and self.date_end <= now:
            result = False
        return result
    
    class Meta:
        abstract = True


class Page(TimeStampedModel, ActivableModel, AbstractDraftable,
           AbstractPublicable, CreatedModifiedBy):
    name = models.CharField(max_length=160,
                            blank=False, null=False)
    webpath = models.ForeignKey(WebPath,
                                on_delete=models.CASCADE,
                                limit_choices_to={'is_active': True},)
    base_template = models.ForeignKey(PageTemplate,
                                      on_delete=models.CASCADE,
                                      limit_choices_to={'is_active': True},)
    description = models.TextField(null=True, blank=True,
                                    help_text=_("Description"
                                                "used for SEO."))
    date_start = models.DateTimeField()
    date_end = models.DateTimeField(null=True, blank=True)
    state = models.CharField(choices=PAGE_STATES, max_length=33,
                             default='draft')

    type = models.CharField(max_length=33,
                            default="standard",
                            choices=(('standard', _('Page')),
                                     ('home', _('Home Page'))))
    tags = TaggableManager()

    class Meta:
        verbose_name_plural = _("Pages")


    def get_blocks(self, section=None):
        query_params = dict(is_active=True)
        if section:
            query_params['section'] = section
        blocks = PageBlock.objects.filter(page=self,
                                          **query_params).\
                                   order_by('section', 'order').\
                                   values_list('order', 'block__pk')
        template_blocks = self.base_template.\
                            pagetemplateblock_set.\
                            filter(**query_params).\
                            order_by('section', 'order').\
                            values_list('order', 'block__pk')
        excluded_blocks = PageBlock.objects.filter(page=self,
                                                   is_active=False).\
                                   values_list('block__pk', flat=True)
        order_pk = []
        # CHECK concurrent ordering sorting
        for i in blocks:
            order_pk.append(i)
        for i in template_blocks:
            # check if a template blocks has not been disabled in the page
            if i[1] not in excluded_blocks:
                order_pk.append(i)
        ordered = sorted(order_pk)
        unique = []
        for i in ordered:
            if i[1] not in unique:
                unique.append(i)
        final_blocks = [TemplateBlock.objects.get(pk=v)
                        for k,v in unique]
        return final_blocks


    def delete(self, *args, **kwargs):
        PageRelated.objects.filter(related_page=self).delete()
        super(self.__class__, self).delete(*args, **kwargs)


    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)

        for rel in PageRelated.objects.filter(page=self):
            if not PageRelated.objects.\
                    filter(page=rel.related_page, related_page=self):
                PageRelated.objects.\
                    create(page=rel.page, related_page=self,
                           is_active=True)

    def get_category_img(self):
        return [i.image_as_html() for i in self.category.all()]

    def __str__(self):
        return '{} {}'.format(self.name, self.state)


class PageCarousel(SectionAbstractModel, ActivableModel, SortableModel,
                   TimeStampedModel):
    page = models.ForeignKey(Page, null=False, blank=False,
                             on_delete=models.CASCADE)
    carousel = models.ForeignKey(Carousel, null=False, blank=False,
                                 on_delete=models.CASCADE)


    class Meta:
        verbose_name_plural = _("Page Carousel")

    def __str__(self):
        return '{} {} :{}'.format(self.page, self.carousel,
                                  self.section or '#')


class PageMenu(SectionAbstractModel, ActivableModel, SortableModel,
               TimeStampedModel):
    page = models.ForeignKey(Page, null=False, blank=False,
                             on_delete=models.CASCADE)
    menu = models.ForeignKey(NavigationBar, null=False, blank=False,
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = _("Page Navigation Bars")

    def __str__(self):
        return '{} {} :{}'.format(self.page, self.menu,
                                  self.section or '#')


class PageBlock(ActivableModel, SectionAbstractModel, SortableModel):
    page = models.ForeignKey(Page, null=False, blank=False,
                             on_delete=models.CASCADE)
    block = models.ForeignKey(TemplateBlock, null=False, blank=False,
                              on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = _("Page Block")

    def __str__(self):
        return '{} {} {}:{}'.format(self.page,
                                    self.block.name,
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
        return '{} {}'.format(self.page, self.name)


class AbstractPublication(TimeStampedModel, ActivableModel):
    CONTENT_TYPES = (('markdown', 'markdown'),
                     ('html', 'html'))

    title   = models.CharField(max_length=256,
                               null=False, blank=False,
                               help_text=_("Heading, Headline"))

    subheading        = models.TextField(max_length=1024,
                                         null=True,blank=True,
                                         help_text=_("Strap line (press)"))
    content           =  models.TextField(null=True,blank=True,
                                          help_text=_('Content'))
    content_type     = models.CharField(choices=CONTENT_TYPES,
                                        null=False, blank=False,
                                        max_length=33,
                                        default='markdown')
    presentation_image = models.ForeignKey(Media, null=True, blank=True,
                                           on_delete=models.CASCADE)
    state             = models.CharField(choices=PAGE_STATES,
                                         max_length=33,
                                         default='draft')
    date_start        = models.DateTimeField()
    date_end          = models.DateTimeField()
    category          = models.ManyToManyField('Category')

    note    = models.TextField(null=True,blank=True,
                               help_text=_('Editorial Board notes'))

    class Meta:
        abstract = True
        indexes = [
           models.Index(fields=['title']),
        ]


class Category(TimeStampedModel, CreatedModifiedBy):
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


class Publication(AbstractPublication, AbstractPublicable, 
                  CreatedModifiedBy):
    slug = models.SlugField(null=True, blank=True)
    tags = TaggableManager()
    relevance = models.IntegerField(default=0, blank=True)
    
    class Meta:
        verbose_name_plural = _("Publications")

    def serialize(self):
        return {'slug': self.slug,
                'image': self.image_url(),
                'title': self.title,
                'published': self.date_start,
                'subheading': self.subheading,
                'categories': (i.name for i in self.categories),
                'tags': (i.name for i in self.tags.all()),
                'published_in': (f'{i.webpath.site}{i.webpath.fullpath}'
                                 for i in self.publicationcontext_set.all())}

    def active_translations(self):
        return PublicationLocalization.objects.filter(publication=self,
                                                      is_active=True)

    def image_url(self):
        if self.presentation_image:
            image_path =  self.presentation_image.file
        else:
            image_path = self.category.first().image
        return sanitize_path(f'{settings.MEDIA_URL}/{image_path}')

    @property
    def categories(self):
        return self.category.all()

    @property
    def related_publications(self):
        related = PublicationRelated.objects.filter(publication=self,
                                                    related__is_active=True)
        return [i for i in related if i.related.is_publicable]

    @property
    def related_contexts(self):
        return PublicationContext.objects.filter(publication=self,
                                                 webpath__is_active=True)
    
    @property
    def first_available_url(self):
        pubcontx = PublicationContext.objects.filter(publication=self,
                                                     webpath__is_active=True)
        if pubcontx:
            return pubcontx.first().url
    
    @property
    def related_links(self):
        return self.publicationlink_set.all()

    @property
    def related_galleries(self):
        return PublicationGallery.objects.filter(publication=self,
                                                 is_active=True)

    def translate_as(self, lang):
        """
        returns translation if available
        """
        trans = PublicationLocalization.objects.filter(publication=self,
                                                       language=lang,
                                                       is_active=True).first()
        if trans:
            self.title = trans.title
            self.subheading = trans.subheading
            self.content = trans.content

    @property
    def available_in_languages(self) -> list:
        return [(i, i.get_language_display())
                for i in
                PublicationLocalization.objects.filter(publication=self,
                                                       is_active=True)]


    def title2slug(self):
        return slugify(self.title)

    def delete(self, *args, **kwargs):
        super(self.__class__, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.title2slug()
        super(self.__class__, self).save(*args, **kwargs)
        
        
    def get_attachments(self):
        return PublicationAttachment.objects.filter(publication=self,
                                                    is_active=True).\
                                             order_by('order')

    def __str__(self):
        return '{} {}'.format(self.title, self.state)


class PublicationContext(TimeStampedModel, ActivableModel,
                         SectionAbstractModel, SortableModel,
                         CreatedModifiedBy):
    publication = models.ForeignKey(Publication, null=False, blank=False,
                                    on_delete=models.CASCADE)
    webpath = models.ForeignKey(WebPath, on_delete=models.CASCADE)
    in_evidence_start = models.DateTimeField(null=True,blank=True)
    in_evidence_end   = models.DateTimeField(null=True,blank=True)

    class Meta:
        verbose_name_plural = _("Publication Contexts")

    @property
    def path_prefix(self):
        return getattr(settings, 'CMS_PUBLICATION_VIEW_PREFIX_PATH',
                                 CMS_PUBLICATION_VIEW_PREFIX_PATH)

    def get_url_list(self, category_name=None):
        list_prefix = getattr(settings, 'CMS_PUBLICATION_LIST_PREFIX_PATH',
                                         CMS_PUBLICATION_LIST_PREFIX_PATH)
        url = sanitize_path(f'{self.webpath.get_full_path()}/{list_prefix}')
        if category_name:
            url += f'/?category_name={category_name}'
        return sanitize_path(url)

    @property
    def url(self):
        url = f'{self.webpath.get_full_path()}{self.path_prefix}/{self.publication.slug}'
        return sanitize_path(url)

    @property
    def name(self):
        return self.publication.title

    def translate_as(self, *args, **kwargs):
        self.publication.translate_as(*args, **kwargs)

    def serialize(self):
        result = self.publication.serialize()
        result['path'] = self.url
        return result

    def __str__(self):
        return '{} {}'.format(self.publication, self.webpath)


class PublicationLink(TimeStampedModel):
    publication = models.ForeignKey(Publication, null=False, blank=False,
                                    on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=False, blank=False)
    url = models.URLField(help_text=_("url"))

    class Meta:
        verbose_name_plural = _("Publication Links")

    def __str__(self):
        return '{} {}'.format(self.publication, self.name)


class PublicationBlock(TimeStampedModel, ActivableModel, SortableModel):
    publication = models.ForeignKey(Publication, null=False, blank=False,
                                    on_delete=models.CASCADE)
    block = models.ForeignKey(TemplateBlock, null=False, blank=False,
                              on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = _("Publication Page Block")

    def __str__(self):
        return '{} {} {}:{}'.format(self.publication,
                                    self.block.name,
                                    self.order or '#',
                                    self.section or '#')


class PublicationGallery(TimeStampedModel, ActivableModel, SortableModel):
    publication = models.ForeignKey(Publication,
                                    on_delete=models.CASCADE)
    collection = models.ForeignKey(MediaCollection,
                                    on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = _("Publication Image Gallery")

    def __str__(self):
        return '{} {}'.format(self.publication, self.collection)


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


def publication_attachment_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'publications_attachments/{}/{}'.format(instance.publication.pk,
                                                   filename)


class PublicationAttachment(TimeStampedModel, SortableModel, ActivableModel,
                            AbstractMedia):

    publication = models.ForeignKey(Publication, null=False, blank=False,
                                    related_name='page_attachment',
                                    on_delete=models.CASCADE)
    name = models.CharField(max_length=60, blank=True, null=True,
                    help_text=_("Specify the container "
                                "section in the template where "
                                "this block would be rendered."))
    file = models.FileField(upload_to=publication_attachment_path)
    description = models.TextField()


    class Meta:
        verbose_name_plural = _("Publication Attachments")

    
    def __str__(self):
        return '{} {} ({})'.format(self.publication, self.name,
                                   self.file_type)


class PublicationLocalization(TimeStampedModel, ActivableModel,
                              CreatedModifiedBy):
    title   = models.CharField(max_length=256,
                               null=False, blank=False,
                               help_text=_("Heading, Headline"))
    publication = models.ForeignKey(Publication,
                                    null=False, blank=False,
                                    on_delete=models.CASCADE)
    language = models.CharField(choices=settings.LANGUAGES,
                                max_length=12, null=False,blank=False,
                                default='en')
    subheading = models.TextField(max_length=1024,
                                  null=True,blank=True,
                                  help_text=_("Strap line (press)"))
    content =  models.TextField(null=True,blank=True,
                                        help_text=_('Content'))
    class Meta:
        verbose_name_plural = _("Publication Localizations")

    def __str__(self):
        return '{} {}'.format(self.publication, self.language)