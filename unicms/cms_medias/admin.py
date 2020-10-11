from django.contrib import admin

from . models import *


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display  = ('context', 'name', 'file_size', 'file_format')
    list_filter   = ('context__site__domain', 'file_format', 
                     'created', 'modified')
    readonly_fields = ('created_by', 'modified_by', 
                       'file_size', 'file_format')


@admin.register(MediaCollection)
class MediaCollectionAdmin(admin.ModelAdmin):
    search_fields = ('name',)
