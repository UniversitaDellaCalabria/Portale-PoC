import nested_admin
from django.contrib import admin

from . models import *


class NavigationBarItemLocalizationInline(nested_admin.NestedStackedInline):
    model = NavigationBarItemLocalization
    extra = 0
    classes = ['collapse']
    sortable_field_name = ""


class NavigationBarItemInline(nested_admin.NestedStackedInline):
    model = NavigationBarItem
    autosearch_fields = ('parent', )
    raw_id_fields = ('publication',)
    extra = 0
    classes = ['collapse']
    inlines = (NavigationBarItemLocalizationInline,)
    sortable_field_name = "order"
    readonly_fields = ('created_by', 'modified_by',)


@admin.register(NavigationBar)
class NavigationBarAdmin(nested_admin.NestedModelAdmin):
    list_display  = ('context', 'name', 'section', 'is_active')
    search_fields   = ('context', 'name',)
    list_filter = ('context__site__domain', 
                   'created', 'modified')
    readonly_fields = ('created_by', 'modified_by')
    inlines = (NavigationBarItemInline,)
    raw_id_fields = ('context', )


@admin.register(NavigationBarItem)
class NavigationBarItemAdmin(nested_admin.NestedModelAdmin):
    list_display  = ('menu', 'name', 'parent', 'is_active')
    search_fields   = ('menu__context__name', 'name',)
    list_filter = ('menu__context__site__domain', 
                   'created', 'modified')
    readonly_fields = ('created_by', 'modified_by')
    inlines = (NavigationBarItemLocalizationInline,)
    raw_id_fields = ('menu', )
