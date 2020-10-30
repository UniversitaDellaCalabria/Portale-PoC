from django.db import models
from django.utils.translation import gettext_lazy as _

from cms.models import Page
from cms_context.models import *
from cms_templates.models import (CMS_TEMPLATE_BLOCK_SECTIONS,
                                  ActivableModel,
                                  SectionAbstractModel,
                                  SortableModel,
                                  TimeStampedModel)

class NavigationBar(TimeStampedModel, ActivableModel, SectionAbstractModel):
    context = models.ForeignKey(WebPath,
                            on_delete=models.CASCADE,
                            limit_choices_to={'is_active': True},)
    name = models.CharField(max_length=33, blank=False, null=False)
    created_by = models.ForeignKey(get_user_model(),
                                   null=True, blank=True,
                                   on_delete=models.CASCADE,
                                   related_name='menu_created_by')
    modified_by = models.ForeignKey(get_user_model(),
                                    null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='menu_modified_by')
    
    class Meta:
        verbose_name_plural = _("Context Navigation Menus")


    def get_localized_items(self, lang=settings.LANGUAGE, **kwargs):
        items = []
        for i in NavigationBarItem.objects.filter(menu=self,
                                                  is_active=True,
                                                  **kwargs).\
                                           order_by('order'):
            items.append(i.localized(lang=lang))
        return items
    
    def __str__(self):
        return '{} - {}'.format(self.context, self.name)


class NavigationBarItem(TimeStampedModel, SortableModel, ActivableModel):
    """
    elements that builds up the navigation menu
    """
    menu = models.ForeignKey(NavigationBar,
                             null=True, blank=True,
                             on_delete=models.CASCADE,
                             related_name="related_menu")
    name = models.CharField(max_length=33, blank=False, null=False)
    page = models.ForeignKey(Page,
                             null=True, blank=True,
                             on_delete=models.CASCADE,
                             related_name="linked_page")
    parent = models.ForeignKey('NavigationBarItem',
                               null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name="related_parent")
    url = models.CharField(help_text=_("url"),
                           null=True, blank=True, max_length=2048)
    publication = models.ForeignKey('cms.Publication',
                                    null=True, blank=True,
                                    related_name='pub',
                                    on_delete=models.CASCADE)
    created_by = models.ForeignKey(get_user_model(),
                                   null=True, blank=True,
                                   on_delete=models.CASCADE,
                                   related_name='menu_item_created_by')
    modified_by = models.ForeignKey(get_user_model(),
                                    null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='menu_item_modified_by')
    class Meta:
        verbose_name_plural = _("Context Navigation Menu Items")

    @property
    def link(self):
        return self.url or self.page or self.publication or '#'

    def localized(self, lang=settings.LANGUAGE, **kwargs):
        i18n = NavigationBarItemLocalization.objects.filter(item=self,
                                                            language=lang).first()
        if i18n:
            self.name = i18n.name
            self.language = lang
        else:
            self.language = None
        return self

    def get_childs(self, lang=settings.LANGUAGE):
        items = NavigationBarItem.objects.filter(is_active=True,
                                                 parent=self,
                                                 menu=self.menu).\
                                          order_by('order')
        if getattr(self, 'language', lang):
            for item in items:
                i18n = NavigationBarItemLocalization.objects.filter(item=self,
                                                                    language=lang).first()
                if i18n:
                    item.name = i18n
        return items


    def __str__(self):
        return '{} - {} {}'.format(self.menu,
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
