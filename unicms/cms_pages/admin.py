from django.contrib import admin

from . admin_inlines import *
from . models import *


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display  = ('context', 'name', 
                     'date_start', 'date_end', 
                     'is_active',)
    list_filter   = ('state', 'is_active', 'type',
                     'created', 'modified', 'date_start', 'date_end')
    readonly_fields = ('created_by', 'modified_by')
    inlines       = (PageBlockInline, PageThirdPartyBlockInline,
                     PageRelatedInline, PageLinkInline)
