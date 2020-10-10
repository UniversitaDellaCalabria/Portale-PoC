from django.contrib import admin

from . models import *


class PageBlockTemplateInline(admin.TabularInline):
    model = PageBlockTemplate
    extra = 0
    classes = ['collapse']


class PageTemplateThirdPartyBlockInline(admin.TabularInline):
    model = PageTemplateThirdPartyBlock
    extra = 0
    classes = ['collapse']
