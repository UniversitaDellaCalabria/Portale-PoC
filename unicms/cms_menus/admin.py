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
    raw_id_fields = ('parent', 'page', 'publication')
    extra = 0
    # classes = ['collapse']
    inlines = (NavigationBarItemLocalizationInline,)
    sortable_field_name = "order"
    readonly_fields = ('created_by', 'modified_by',)


@admin.register(NavigationBar)
class NavigationBarAdmin(nested_admin.NestedModelAdmin):
    list_display  = ('name', 'is_active')
    search_fields   = ('name',)
    list_filter = ('created', 'modified')
    readonly_fields = ('created_by', 'modified_by')
    inlines = (NavigationBarItemInline,)


@admin.register(NavigationBarItem)
class NavigationBarItemAdmin(nested_admin.NestedModelAdmin):
    list_display  = ('menu', 'name', 'parent', 'is_active')
    search_fields   = ('name',)
    list_filter = ('created', 'modified')
    readonly_fields = ('created_by', 'modified_by')
    inlines = (NavigationBarItemLocalizationInline,)
    raw_id_fields = ('menu', )
