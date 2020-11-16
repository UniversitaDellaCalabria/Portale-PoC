from django.contrib import admin

from . admin_inlines import *
from . models import *
from . forms import *


class AbstractCreateModifiedBy(admin.ModelAdmin):
    readonly_fields = ('created_by', 'modified_by')


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display  = ('webpath', 'name',
                     'date_start', 'date_end',
                     'is_active',)
    list_filter   = ('state', 'is_active', 'type',
                     'created', 'modified', 'date_start', 'date_end')
    readonly_fields = ('created_by', 'modified_by')
    inlines       = (PageMenuInline,
                     PageCarouselInline, PageBlockInline, 
                     PageThirdPartyBlockInline,
                     PageRelatedInline, PageLinkInline)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'image_as_html')

    def delete_model(modeladmin, request, queryset):
        obj.delete()


@admin.register(Publication)
class PublicationAdmin(AbstractCreateModifiedBy):
    search_fields = ('title',)
    list_display  = ('title', 'slug', 'date_start', 'date_end', 'is_active',)
    list_filter   = ('state', 'is_active',
                     'created', 'modified', 'date_start', 'date_end')
    inlines       = (PublicationLocalizationInline,
                     PublicationContextInline,
                     PublicationRelatedInline,
                     PublicationLinkInline,
                     PublicationAttachmentInline,
                     PublicationGalleryInline)
    raw_id_fields = ('presentation_image',)


@admin.register(PublicationLocalization)
class PublicationLocalizationAdmin(AbstractCreateModifiedBy):
    search_fields = ('publication__title',)
    list_display  = ('publication', 'language', 'is_active',)
    list_filter   = ('publication__state', 'is_active',
                     'created', 'modified', 'language')
