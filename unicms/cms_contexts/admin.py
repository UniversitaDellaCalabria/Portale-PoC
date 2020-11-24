import json

from copy import deepcopy
from django.contrib import admin
from django.contrib import messages
from django.forms.utils import ErrorList
from django.http import (HttpResponse,
                         Http404,
                         HttpResponseBadRequest,
                         HttpResponseRedirect)
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext, gettext_lazy as _

from . models import *


admin.site.unregister(Site)


class WebPathAdminInline(admin.TabularInline):
    model = WebPath
    extra = 0


class AbstractPreviewableAdmin(admin.ModelAdmin):
    change_form_template = "change_form_preview.html"

    def response_change(self, request, obj):
        if "_save_draft" in request.POST:
            _msg = ("Draft of '{}' [{}] been created. You can preview it if is_active=True "
                    "and 'Draft view mode' is set on.").format(obj, obj.pk)
            draft = obj.__dict__.copy()
            draft['state'] = 'draft'
            draft['draft_of'] = obj.pk
            for attr in "id pk _state created_by modified_by created modified".split(' '):
                if draft.get(attr):
                    draft.pop(attr)
                
            new_obj = obj.__class__.objects.create(**draft)
            tags = [i for i in obj.tags.values_list('name', flat=1)]
            new_obj.tags.add(*tags)
            
            self.message_user(request, _msg)
            url = reverse('admin:cms_page_change', 
                          kwargs={'object_id': new_obj.pk})
            return HttpResponseRedirect(url)  
        
        elif request.POST.get('state') == 'published' and obj.draft_of:
            published = obj.__class__.filter(pk=obj.draft_of).first()
            if not published:
                self.message_user(request, 
                                  "Draft missed its parent page ... ",
                                  level = messages.ERROR)
            published.is_active = False
            obj.is_active = True
            obj.draft_of = None
            published.save()
            obj.save()
            
            self.message_user(request, "Draft being published succesfully")
            
        
        elif "_preview" in request.POST:
            # matching_names_except_this = self.get_queryset(request).filter(name=obj.name).exclude(pk=obj.id)
            # matching_names_except_this.delete()
            # obj.is_unique = True
            # obj.save()
            self.message_user(request, "Preview is available at ...")
            return HttpResponseRedirect(".")
            
        return super().response_change(request, obj)


@admin.register(WebSite)
class WebSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('domain', 'name')


class EditorialBoardEditorsAdminInline(admin.TabularInline):
    model = EditorialBoardEditors
    extra = 0
    readonly_fields = ('created', 'modified')
    raw_id_fields = ('user', 'webpath')


@admin.register(WebPath)
class WebPathAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'site', 'is_active')
    list_filter = ('site', 'created', 'modified', 'is_active')
    search_fields = ('name', 'path',)
    readonly_fields = ('fullpath', 'created', 'modified')
    inlines = (EditorialBoardEditorsAdminInline,)


@admin.register(EditorialBoardEditors)
class EditorialBoardEditorsAdmin(admin.ModelAdmin):
    list_display = ('user', 'permission', 'webpath', 'is_active')
    list_filter = ('permission', 'created', 'modified', 'is_active')
    search_fields = ('user', )
    readonly_fields = ('created', 'modified')


@admin.register(EditorialBoardLocks)
class EditorialBoardLocksAdmin(admin.ModelAdmin):
    list_filter = ('locked_time', )
    list_display = ('content_type', 'object_id', 
                    'is_active', 'locked_time', 'locked_by')
