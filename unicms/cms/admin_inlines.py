from django.contrib import admin

from . models import *


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
    raw_id_fields = ('block',)
    

class PublicationContextInline(admin.TabularInline):
    model = PublicationContext
    extra = 0
    classes = ['collapse']
    readonly_fields = ('created_by', 'modified_by')


class PublicationLocalizationInline(admin.StackedInline):
    model = PublicationLocalization
    extra = 0
    classes = ['collapse']


class PublicationRelatedInline(admin.StackedInline):
    model = PublicationRelated
    extra = 0
    fk_name = 'publication'
    classes = ['collapse']
    raw_id_fields = ('related',)


class PublicationAttachmentInline(admin.StackedInline):
    model = PublicationAttachment
    extra = 0
    classes = ['collapse']
    readonly_fields = ('file_size', 'file_type')


class PublicationLinkInline(admin.StackedInline):
    model = PublicationLink
    extra = 0
    fk_name = 'publication'
    classes = ['collapse']


class PublicationGalleryInline(admin.StackedInline):
    model = PublicationGallery
    extra = 0
    classes = ['collapse']
    raw_id_fields = ['collection']


class PublicationBlockInline(admin.TabularInline):
    model = PublicationBlock
    extra = 0
    classes = ['collapse']
    raw_id_fields = ['block']


class PageCarouselInline(admin.TabularInline):
    model = PageCarousel
    extra = 0
    classes = ['collapse']
    raw_id_fields = ("carousel",)


class PageMenuInline(admin.TabularInline):
    model = PageMenu
    extra = 0
    classes = ['collapse']
    raw_id_fields = ("menu",)
