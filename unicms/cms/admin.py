from django.contrib import admin

from . admin_inlines import *
from . models import *
from . forms import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'image_as_html')
    inlines = (SubCategoryAdminInline, )


#  @admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'category')
    list_filter   = ('category',)


@admin.register(PageTemplate)
class PageTemplateAdmin(admin.ModelAdmin):
    list_display  = ('name', 'template_file', 'created', 'is_active')
    search_fields   = ('name', 'template_file',)
    inlines       = (PageBlockTemplateInline, )


@admin.register(PageBlockTemplate)
class PageBlockTemplateAdmin(admin.ModelAdmin):
    list_display  = ('name', 'template', 'is_active')
    search_fields   = ('name', 'template',)


@admin.register(ContextBasePageTemplate)
class ContextBasePageTemplateAdmin(admin.ModelAdmin):
    list_display  = ('name', 'context', 'template', 'is_active')
    search_fields   = ('name', 'template',)
    list_filter = ('context', )
    inlines = (ContextNavBarItemInline, PageInline,)


@admin.register(ContextNavBarItem)
class ContextNavBarItemAdmin(admin.ModelAdmin):
    list_display  = ('context', 'name', 'parent', 'is_active')
    search_fields   = ('context', 'name', 'parent',)
    list_filter = ('context', 'created', 'modified')


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    search_fields = ('slug',)
    list_display  = ('context', 'slug', 'is_active',)
    list_filter   = ('state', 'is_active', 'category',
                     'created', 'modified', 'date_start', 'date_end')
    inlines       = (PageBlockInline, PageRelatedInline, 
                     PageLinkInline, PageThirdPartyBlockInline)
