import json

from django.contrib import admin
from django.contrib import messages
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django.utils.translation import gettext, gettext_lazy as _

from . models import *


class EditorialBoardContextAdminInline(admin.TabularInline):
    model = EditorialBoardContext
    extra = 0


class EditorialBoardEditorsAdminInline(admin.TabularInline):
    model = EditorialBoardEditors
    extra = 0
    readonly_fields = ('created', 'modified')
    autocomplete_fields = ('user', 'context')


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('fqdn', 'is_active')
    list_filter = ('created', 'modified', 'is_active')
    search_fields = ('fqdn',)
    readonly_fields = ('created', 'modified')
    inlines = [EditorialBoardContextAdminInline,]


@admin.register(EditorialBoardContext)
class EditorialBoardContextAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'site', 'is_active')
    list_filter = ('site', 'created', 'modified', 'is_active')
    search_fields = ('name', 'path',)
    readonly_fields = ('created', 'modified')
    inlines = (EditorialBoardEditorsAdminInline,)


@admin.register(EditorialBoardEditors)
class EditorialBoardEditorsAdmin(admin.ModelAdmin):
    list_display = ('user', 'permission', 'context', 'is_active')
    list_filter = ('permission', 'created', 'modified', 'is_active')
    search_fields = ('user', )
    readonly_fields = ('created', 'modified')
