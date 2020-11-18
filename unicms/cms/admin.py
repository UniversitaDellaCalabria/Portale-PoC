import logging

from django.contrib import admin
from django.contrib import messages
from django.utils.module_loading import import_string

from . admin_inlines import *
from . models import *
from . forms import *


logger = logging.getLogger(__name__)


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
                     PageRelatedInline, PageLinkInline)
    
    def save_model(self, request, obj, form, change):
        super(PageAdmin, self).save_model(request, obj, form, change)
        for block_entry in obj.pageblock_set.filter(is_active=True):
            # Block rendering validation
            block = import_string(block_entry.block.type)(content=block_entry.block.content,
                                                          request=request,
                                                          page=obj,
                                                          webpath=obj.webpath)
            try:
                block.render()
            except Exception as e:
                block_entry.is_active = False
                block_entry.save()
                messages.add_message(request, messages.ERROR, f'{block_entry} failed validation on save')
                logger.exception('ADMIN VALIDATION: Block {} failed rendering ({}): {}'.format(block_entry, obj, e))
    

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
