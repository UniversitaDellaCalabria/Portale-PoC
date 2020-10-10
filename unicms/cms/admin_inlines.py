from django.contrib import admin

from . models import *


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
