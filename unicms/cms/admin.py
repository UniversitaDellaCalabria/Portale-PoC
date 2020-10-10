from django.contrib import admin

from . admin_inlines import *
from . models import *
from . forms import *


class AbstractCreateModifiedBy(admin.ModelAdmin):
    readonly_fields = ('created_by', 'modified_by')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'image_as_html')
    # inlines = (SubCategoryAdminInline, )
    
    def delete_model(modeladmin, request, queryset):
        obj.delete()

# @admin.register(SubCategory)
# class SubCategoryAdmin(admin.ModelAdmin):
    # list_display  = ('name', 'category')
    # list_filter   = ('category',)


@admin.register(PageTemplate)
class PageTemplateAdmin(admin.ModelAdmin):
    list_display  = ('name', 'template_file', 'created', 'is_active')
    search_fields   = ('name', 'template_file',)
    inlines       = (PageBlockTemplateInline,
                     PageTemplateThirdPartyBlockInline)


@admin.register(PageBlockTemplate)
class PageBlockTemplateAdmin(admin.ModelAdmin):
    list_display  = ('name', 'template', 'is_active')
    search_fields   = ('name', 'template',)


@admin.register(ContextNavBarItem)
class ContextNavBarItemAdmin(admin.ModelAdmin):
    list_display  = ('context', 'name', 'parent', 'is_active')
    search_fields   = ('context', 'name', 'parent',)
    list_filter = ('context', 'created', 'modified')


#  @admin.register(PageTemplateThirdPartyBlock)
class PageTemplateThirdPartyBlockAdmin(admin.ModelAdmin):
    list_display  = ('context', 'block', 'section', 'is_active')
    #  search_fields   = ('context', 'name', 'parent',)
    list_filter = ('context', 'created', 'modified')


@admin.register(Page)
class PageAdmin(AbstractCreateModifiedBy):
    search_fields = ('name',)
    list_display  = ('context', 'name', 
                     'date_start', 'date_end', 
                     'is_active',)
    list_filter   = ('state', 'is_active', 'category',
                     'created', 'modified', 'date_start', 'date_end')
    inlines       = (PageBlockInline, PageThirdPartyBlockInline,
                     PageRelatedInline, PageLinkInline)


@admin.register(ContextPublication)
class ContextPublicationAdmin(AbstractCreateModifiedBy):
    search_fields = ('title',)
    list_display  = ('title', 'slug', 'is_active',)
    list_filter   = ('state', 'is_active',
                     'created', 'modified', 'date_start', 'date_end')
    inlines       = (ContextPublicationLocalizationInline,
                     ContextPublicationRelatedInline,
                     ContextPublicationAttachmentInline)


@admin.register(ContextPublicationLocalization)
class ContextPublicationLocalizationAdmin(AbstractCreateModifiedBy):
    search_fields = ('context_publication__title',)
    list_display  = ('context_publication', 'language', 'is_active',)
    list_filter   = ('context_publication__state', 'is_active', 
                     'created', 'modified', 'language')


@admin.register(ContextMedia)
class ContextMediaAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display  = ('context', 'name', 'file_size', 'file_format')
    list_filter   = ('context__site__fqdn', 'file_format', 
                     'created', 'modified')
    readonly_fields = AbstractCreateModifiedBy.readonly_fields + ('file_size', 'file_format')


@admin.register(ContextMediaCollection)
class ContextMediaCollectionAdmin(admin.ModelAdmin):
    search_fields = ('name',)
