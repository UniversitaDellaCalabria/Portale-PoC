from django.contrib import admin

from . admin_inlines import *
from . models import *
from . forms import *


class AbstractCreateModifiedBy(admin.ModelAdmin):
    readonly_fields = ('created_by', 'modified_by')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'image_as_html')
    
    def delete_model(modeladmin, request, queryset):
        obj.delete()


@admin.register(NavigationBarItem)
class NavigationBarItemAdmin(admin.ModelAdmin):
    list_display  = ('context', 'name', 'parent', 'order', 'is_active')
    search_fields   = ('context', 'name', 'parent',)
    list_filter = ('context__site', 'created', 'modified')


@admin.register(Publication)
class PublicationAdmin(AbstractCreateModifiedBy):
    search_fields = ('title',)
    list_display  = ('title', 'slug', 'is_active',)
    list_filter   = ('state', 'is_active',
                     'created', 'modified', 'date_start', 'date_end')
    inlines       = (PublicationLocalizationInline,
                     PublicationRelatedInline,
                     PublicationLinkInline,
                     PublicationAttachmentInline)


@admin.register(PublicationLocalization)
class PublicationLocalizationAdmin(AbstractCreateModifiedBy):
    search_fields = ('context_publication__title',)
    list_display  = ('context_publication', 'language', 'is_active',)
    list_filter   = ('context_publication__state', 'is_active', 
                     'created', 'modified', 'language')
