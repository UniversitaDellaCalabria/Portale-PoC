from django.contrib import admin

from . models import *


class PageInline(admin.TabularInline):
    model = Page
    extra = 0
    classes = ['collapse']


class PageLinkInline(admin.TabularInline):
    model = PageLink
    extra = 0
    classes = ['collapse']


class PageRelatedInline(admin.TabularInline):
    model = PageRelated
    fk_name = 'page'
    autocomplete_fields = ('related_page',)
    extra = 0
    classes = ['collapse']


class PageBlockInline(admin.TabularInline):
    model = PageBlock
    extra = 0


class PageThirdPartyBlockInline(admin.TabularInline):
    model = PageThirdPartyBlock
    extra = 0
    classes = ['collapse']
