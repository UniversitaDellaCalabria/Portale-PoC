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
    list_display  = ('name', 'path', 'created', 'is_active')
    search_fields   = ('name', 'path',)


@admin.register(BlockTemplate)
class BlockTemplateAdmin(admin.ModelAdmin):
    list_display  = ('name', 'path', 'is_active')
    search_fields   = ('name', 'path',)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    search_fields = ('slug',)
    list_display  = ('context', 'slug', 'is_active',)
    list_filter   = ('category', 'state', 'is_active',
                     'created', 'modified', 'date_start', 'date_end')
    inlines       = (PageBlockInline, PageRelatedInline, PageLinkInline, )
