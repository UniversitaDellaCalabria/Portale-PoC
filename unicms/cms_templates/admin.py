from django.contrib import admin

from . admin_inlines import *
from . models import *


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


#  @admin.register(PageTemplateThirdPartyBlock)
class PageTemplateThirdPartyBlockAdmin(admin.ModelAdmin):
    list_display  = ('context', 'block', 'section', 'is_active')
    #  search_fields   = ('context', 'name', 'parent',)
    list_filter = ('context', 'created', 'modified')
