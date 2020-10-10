import logging

from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from . import settings as app_settings

logger = logging.getLogger(__name__)

CMS_BLOCK_SCHEMAS = getattr(settings, 'CMS_BLOCK_SCHEMAS',
                            app_settings.CMS_BLOCK_SCHEMAS)
CMS_BLOCK_TEMPLATES = getattr(settings, 'CMS_BLOCK_TEMPLATES',
                            app_settings.CMS_BLOCK_TEMPLATES)
CMS_TEMPLATE_BLOCK_SECTIONS = getattr(settings, 'CMS_TEMPLATE_BLOCK_SECTIONS',
                                      app_settings.CMS_TEMPLATE_BLOCK_SECTIONS)
CMS_PAGE_TEMPLATES = getattr(settings, 'CMS_PAGE_TEMPLATES',
                            app_settings.CMS_PAGE_TEMPLATES)


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified =  models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SortableModel(models.Model):
    order = models.IntegerField(null=True, blank=True, default=10)

    class Meta:
        abstract = True
        ordering = ['order']


class ActivableModel(models.Model):
    is_active    = models.BooleanField()

    class Meta:
        abstract = True


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
    block = models.ForeignKey('cms_pages.PageBlock', null=False, blank=False,
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