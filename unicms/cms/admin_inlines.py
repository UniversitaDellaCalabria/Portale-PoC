from django.contrib import admin

from . models import *


class NavigationBarItemLocalizationInline(admin.TabularInline):
    model = NavigationBarItemLocalization
    extra = 0
    classes = ['collapse']


class PageInline(admin.TabularInline):
    model = Page
    extra = 0
    classes = ['collapse']


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


class PageBlockInline(admin.TabularInline):
    model = PageBlock
    extra = 0


class PageThirdPartyBlockInline(admin.TabularInline):
    model = PageThirdPartyBlock
    extra = 0
    classes = ['collapse']


class NavigationBarItemInline(admin.TabularInline):
    model = NavigationBarItem
    autocomplete_fields = ('context', 'parent', 'page')
    extra = 0
    classes = ['collapse']


class PublicationLocalizationInline(admin.StackedInline):
    model = PublicationLocalization
    extra = 0
    classes = ['collapse']


class PublicationRelatedInline(admin.StackedInline):
    model = PublicationRelated
    extra = 0
    fk_name = 'publication'
    classes = ['collapse']


class PublicationAttachmentInline(admin.StackedInline):
    model = PublicationAttachment
    extra = 0
    classes = ['collapse']
    readonly_fields = ('file_size', 'file_format')


class PublicationLinkInline(admin.StackedInline):
    model = PublicationLink
    extra = 0
    fk_name = 'publication'
    classes = ['collapse']
