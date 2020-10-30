from django.contrib import admin

from . models import *


class NavigationBarItemInline(admin.TabularInline):
    model = NavigationBarItem
    autocomplete_fields = ('context', 'parent', 'page')
    extra = 0
    classes = ['collapse']


class NavigationBarItemLocalizationInline(admin.TabularInline):
    model = NavigationBarItemLocalization
    extra = 0
    classes = ['collapse']


@admin.register(NavigationBarItem)
class NavigationBarItemAdmin(admin.ModelAdmin):
    list_display  = ('context', 'name', 'parent', 'order', 'is_active')
    search_fields   = ('context', 'name', 'parent',)
    list_filter = ('context__site__domain', 'created', 'modified')
    inlines = (NavigationBarItemLocalizationInline,)
