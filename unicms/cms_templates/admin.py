from django.contrib import admin

from . admin_inlines import *
from . models import *


@admin.register(PageTemplate)
class PageTemplateAdmin(admin.ModelAdmin):
    list_display  = ('name', 'template_file', 'created', 'is_active')
    search_fields   = ('name', 'template_file',)
    inlines       = (PageTemplateThirdPartyBlockInline,)


@admin.register(PageBlockTemplate)
class PageBlockTemplateAdmin(admin.ModelAdmin):
    list_display  = ('name', 'type', 'template_file', 'is_active')
    search_fields   = ('name', 'template_file',)
    list_filter = ('type',)


#  @admin.register(PageTemplateThirdPartyBlock)
class PageTemplateThirdPartyBlockAdmin(admin.ModelAdmin):
    list_display  = ('webpath', 'block', 'section', 'is_active')
    #  search_fields   = ('context', 'name', 'parent',)
    list_filter = ('webpath', 'created', 'modified')
