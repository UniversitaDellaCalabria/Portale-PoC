from django.db import models
from django.utils.translation import gettext_lazy as _

from cms_context.models import *
from cms_templates.models import (CMS_TEMPLATE_BLOCK_SECTIONS,
                                  ActivableModel,
                                  SortableModel,
                                  TimeStampedModel)


class NavigationBarItem(TimeStampedModel, SortableModel, ActivableModel):
    """
    elements that builds up the navigation menu
    """
    context = models.ForeignKey(WebPath,
                                on_delete=models.CASCADE,
                                limit_choices_to={'is_active': True},)
    name = models.CharField(max_length=33, blank=False, null=False)
    page = models.ForeignKey(WebPath,
                             related_name='page_path',
                             on_delete=models.CASCADE,
                             null=True, blank=True)
    parent = models.ForeignKey('NavigationBarItem',
                               null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name="related_page")
    url = models.CharField(help_text=_("url"),
                           null=True, blank=True, max_length=2048)
    publication = models.ForeignKey('cms.Publication',
                                    null=True, blank=True,
                                    related_name='pub',
                                    on_delete=models.CASCADE)
    section = models.CharField(max_length=60, blank=False, null=False,
                               help_text=_("Specify the container "
                                           "section in the template where "
                                           "this menu will be rendered."),
                               choices=CMS_TEMPLATE_BLOCK_SECTIONS)
    created_by = models.ForeignKey(get_user_model(),
                                   null=True, blank=True,
                                   on_delete=models.CASCADE,
                                   related_name='menu_created_by')
    modified_by = models.ForeignKey(get_user_model(),
                                    null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='menu_modified_by')
    class Meta:
        verbose_name_plural = _("Context Navigation Menu Items")

    @property
    def link(self):
        return self.url or self.page or self.publication or '#'

    def get_childs(self):
        return NavigationBarItem.objects.filter(is_active=True,
                                                parent=self,
                                                section=self.section).\
                                         order_by('order')


    def __str__(self):
        return '{} - {} {}'.format(self.context,
                                   self.name, self.parent or '')


class NavigationBarItemLocalization(models.Model):
    item = models.ForeignKey(NavigationBarItem,
                             on_delete=models.CASCADE)
    language   = models.CharField(choices=settings.LANGUAGES,
                                  max_length=12, null=False,blank=False,
                                  default='en')
    name = models.CharField(max_length=33, blank=False, null=False)

    class Meta:
        verbose_name_plural = _("Context Navigation Menu Item Localizations")

    def __str__(self):
        return '{} - {}'.format(self.item, self.language)
