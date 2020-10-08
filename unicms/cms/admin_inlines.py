from django.contrib import admin

from . models import *


class SubCategoryAdminInline(admin.TabularInline):
    model = SubCategory
    extra = 0


class PageLinkInline(admin.TabularInline):
    model = PageLink
    extra = 0


class PageRelatedInline(admin.TabularInline):
    model = PageRelated
    fk_name = 'page'
    autocomplete_fields = ('related_page',)
    extra = 0


class ContextNavBarItemInline(admin.TabularInline):
    model = ContextNavBarItem
    autocomplete_fields = ('context', 'parent', 'page')
    extra = 0


class PageBlockInline(admin.TabularInline):
    model = PageBlock
    extra = 0


class PageThirdPartyBlockInline(admin.TabularInline):
    model = PageThirdPartyBlock
    extra = 0


class PageBlockTemplateInline(admin.TabularInline):
    model = PageBlockTemplate
    extra = 0


class PageTemplateThirdPartyBlockInline(admin.TabularInline):
    model = PageTemplateThirdPartyBlock
    extra = 0


class PageInline(admin.TabularInline):
    model = Page
    extra = 0
