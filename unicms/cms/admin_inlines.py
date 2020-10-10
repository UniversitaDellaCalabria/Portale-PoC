from django.contrib import admin

from . models import *


# class SubCategoryAdminInline(admin.TabularInline):
    # model = SubCategory
    # extra = 0


class PageLinkInline(admin.TabularInline):
    model = PageLink
    extra = 0
    classes = ['collapse']


class PageRelatedInline(admin.TabularInline):
    model = PageRelated
    fk_name = 'page'
    autocomplete_fields = ('related_page',)
    extra = 0
    classes = ['collapse']


class ContextNavBarItemInline(admin.TabularInline):
    model = ContextNavBarItem
    autocomplete_fields = ('context', 'parent', 'page')
    extra = 0
    classes = ['collapse']


class PageBlockInline(admin.TabularInline):
    model = PageBlock
    extra = 0


class PageThirdPartyBlockInline(admin.TabularInline):
    model = PageThirdPartyBlock
    extra = 0
    classes = ['collapse']


class PageBlockTemplateInline(admin.TabularInline):
    model = PageBlockTemplate
    extra = 0
    classes = ['collapse']


class PageTemplateThirdPartyBlockInline(admin.TabularInline):
    model = PageTemplateThirdPartyBlock
    extra = 0
    classes = ['collapse']


class PageInline(admin.TabularInline):
    model = Page
    extra = 0
    classes = ['collapse']


class ContextPublicationLocalizationInline(admin.StackedInline):
    model = ContextPublicationLocalization
    extra = 0
    classes = ['collapse']


class ContextPublicationRelatedInline(admin.StackedInline):
    model = ContextPublicationRelated
    extra = 0
    fk_name = 'publication'
    classes = ['collapse']


class ContextPublicationAttachmentInline(admin.StackedInline):
    model = ContextPublicationAttachment
    extra = 0
    classes = ['collapse']
    readonly_fields = ('file_size', 'file_format')
