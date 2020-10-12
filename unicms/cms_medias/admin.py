from django.contrib import admin

from . models import *


class MediaCollectionItemInline(admin.TabularInline):
    model = MediaCollectionItem
    extra = 0


class MediaLinkInline(admin.TabularInline):
    model = MediaLink
    extra = 0


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display  = ('context', 'title', 'file_size', 'file_format')
    list_filter   = ('context__site__domain', 'file_format', 
                     'created', 'modified')
    readonly_fields = ('created_by', 'modified_by', 
                       'file_size', 'file_format')
    inlines = (MediaCollectionItemInline, MediaLinkInline)


@admin.register(MediaCollection)
class MediaCollectionAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    inlines = (MediaCollectionItemInline,)
