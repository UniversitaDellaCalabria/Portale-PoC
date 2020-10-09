from django.contrib import admin

from . admin_inlines import *
from . models import *
from . forms import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'image_as_html')
    # inlines = (SubCategoryAdminInline, )


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


@admin.register(ContextBasePage)
class ContextBasePageAdmin(admin.ModelAdmin):
    list_display  = ('name', 'context', 'template', 'is_active')
    search_fields   = ('name', 'template',)
    list_filter = ('context', )
    inlines = (ContextNavBarItemInline, PageInline,)


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
class PageAdmin(admin.ModelAdmin):
    search_fields = ('slug',)
    list_display  = ('context', 'slug', 'is_active',)
    list_filter   = ('state', 'is_active', 'category',
                     'created', 'modified', 'date_start', 'date_end')
    inlines       = (PageBlockInline, PageThirdPartyBlockInline,
                     PageRelatedInline, PageLinkInline)


@admin.register(ContextPublication)
class ContextPublicationAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display  = ('title', 'slug', 'is_active',)
    list_filter   = ('state', 'is_active',
                     'created', 'modified', 'date_start', 'date_end')
    inlines       = (ContextPublicationLocalizationInline,)


@admin.register(ContextPublicationLocalization)
class ContextPublicationLocalizationAdmin(admin.ModelAdmin):
    search_fields = ('context_publication__title',)
    list_display  = ('context_publication', 'is_active',)
    list_filter   = ('state', 'is_active', 'category',
                     'created', 'modified', 'date_start', 'date_end',
                     'language')
