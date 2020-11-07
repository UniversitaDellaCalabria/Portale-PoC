import json

from django.contrib import admin
from django.contrib import messages
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django.utils.translation import gettext, gettext_lazy as _

from . models import *


admin.site.unregister(Site)


class WebPathAdminInline(admin.TabularInline):
    model = WebPath
    extra = 0


@admin.register(WebSite)
class WebSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('domain', 'name')


class EditorialBoardEditorsAdminInline(admin.TabularInline):
    model = EditorialBoardEditors
    extra = 0
    readonly_fields = ('created', 'modified')
    autocomplete_fields = ('user', 'context')


@admin.register(WebPath)
class WebPathAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'site', 'is_active')
    list_filter = ('site', 'created', 'modified', 'is_active')
    search_fields = ('name', 'path',)
    readonly_fields = ('fullpath', 'created', 'modified')
    inlines = (EditorialBoardEditorsAdminInline,)


@admin.register(EditorialBoardEditors)
class EditorialBoardEditorsAdmin(admin.ModelAdmin):
    list_display = ('user', 'permission', 'context', 'is_active')
    list_filter = ('permission', 'created', 'modified', 'is_active')
    search_fields = ('user', )
    readonly_fields = ('created', 'modified')
