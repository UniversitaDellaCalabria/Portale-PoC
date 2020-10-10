from django.contrib import admin

from . admin_inlines import *
from . models import *
from . forms import *


class AbstractCreateModifiedBy(admin.ModelAdmin):
    readonly_fields = ('created_by', 'modified_by')


@admin.register(NavigationBarItem)
class NavigationBarItemAdmin(admin.ModelAdmin):
    list_display  = ('context', 'name', 'parent', 'is_active')
    search_fields   = ('context', 'name', 'parent',)
    list_filter = ('context', 'created', 'modified')


@admin.register(Publication)
class PublicationAdmin(AbstractCreateModifiedBy):
    search_fields = ('title',)
    list_display  = ('title', 'slug', 'is_active',)
    list_filter   = ('state', 'is_active',
                     'created', 'modified', 'date_start', 'date_end')
    inlines       = (PublicationLocalizationInline,
                     PublicationRelatedInline,
                     PublicationAttachmentInline)


@admin.register(PublicationLocalization)
class PublicationLocalizationAdmin(AbstractCreateModifiedBy):
    search_fields = ('context_publication__title',)
    list_display  = ('context_publication', 'language', 'is_active',)
    list_filter   = ('context_publication__state', 'is_active', 
                     'created', 'modified', 'language')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display  = ('context', 'name', 'file_size', 'file_format')
    list_filter   = ('context__site__domain', 'file_format', 
                     'created', 'modified')
    readonly_fields = AbstractCreateModifiedBy.readonly_fields + ('file_size', 'file_format')


@admin.register(MediaCollection)
class MediaCollectionAdmin(admin.ModelAdmin):
    search_fields = ('name',)
