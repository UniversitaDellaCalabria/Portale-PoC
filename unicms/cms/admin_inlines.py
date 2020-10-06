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
    extra = 0


class PageBlockInline(admin.TabularInline):
    model = PageBlock
    extra = 0
