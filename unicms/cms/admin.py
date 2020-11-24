import logging

from django.contrib import admin
from django.contrib import messages
from django.http import (HttpResponse,
                         Http404,
                         HttpResponseBadRequest,
                         HttpResponseRedirect)
from django.urls import reverse
from django.utils import timezone
from django.utils.module_loading import import_string
from django.utils.translation import gettext, gettext_lazy as _

from . admin_inlines import *
from . models import *
from . forms import *
from . utils import copy_page_as_draft

logger = logging.getLogger(__name__)


class AbstractCreateModifiedBy(admin.ModelAdmin):
    readonly_fields = ('created_by', 'modified_by')


class AbstractPreviewableAdmin(admin.ModelAdmin):
    change_form_template = "change_form_preview.html"

    def response_change(self, request, obj):
        if "_save_draft" in request.POST:
            _msg = ("Draft of '{}' [{}] been created. You can preview it if is_active=True "
                    "and 'Draft view mode' is set on.").format(obj, obj.pk)
            draft = copy_page_as_draft(obj)
            self.message_user(request, _msg)
            url = reverse('admin:cms_page_change', 
                          kwargs={'object_id': draft.pk})
            return HttpResponseRedirect(url)  
        
        elif request.POST.get('state') == 'published' and obj.draft_of:
            published = obj.__class__.objects.filter(pk=obj.draft_of).first()
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


def make_page_draft(modeladmin, request, queryset):
    for obj in queryset:
        draft = copy_page_as_draft(obj)
make_page_draft.short_description = _("Make page Draft")


@admin.register(Page)
class PageAdmin(AbstractPreviewableAdmin):
    search_fields = ('name',)
    list_display  = ('webpath', 'name',
                     'date_start', 'date_end',
                     'is_active', 'state')
    list_filter   = ('state', 'is_active', 'type',
                     'created', 'modified', 'date_start', 'date_end')
    readonly_fields = ('created_by', 'modified_by', 'draft_of')
    inlines       = (PageMenuInline,
                     PageCarouselInline, PageBlockInline, 
                     PageRelatedInline, PageLinkInline)
    actions = AbstractPreviewableAdmin.actions + [make_page_draft,]
    
    def save_model(self, request, obj, form, change):
        super(PageAdmin, self).save_model(request, obj, form, change)
        for block_entry in obj.pageblock_set.filter(is_active=True):
            # Block rendering validation
            block = import_string(block_entry.block.type)(content=block_entry.block.content,
                                                          request=request,
                                                          page=obj,
                                                          webpath=obj.webpath)
            try:
                block.render()
            except Exception as e:
                block_entry.is_active = False
                block_entry.save()
                messages.add_message(request, messages.ERROR, f'{block_entry} failed validation on save')
                logger.exception('ADMIN VALIDATION: Block {} failed rendering ({}): {}'.format(block_entry, obj, e))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'image_as_html')

    def delete_model(modeladmin, request, queryset):
        obj.delete()


@admin.register(Publication)
class PublicationAdmin(AbstractCreateModifiedBy):
    search_fields = ('title',)
    list_display  = ('title', 'slug', 'date_start', 'date_end', 'is_active',)
    list_filter   = ('state', 'is_active',
                     'created', 'modified', 'date_start', 'date_end')
    inlines       = (PublicationLocalizationInline,
                     PublicationContextInline,
                     PublicationRelatedInline,
                     PublicationLinkInline,
                     PublicationAttachmentInline,
                     PublicationGalleryInline)
    raw_id_fields = ('presentation_image',)


@admin.register(PublicationLocalization)
class PublicationLocalizationAdmin(AbstractCreateModifiedBy):
    search_fields = ('publication__title',)
    list_display  = ('publication', 'language', 'is_active',)
    list_filter   = ('publication__state', 'is_active',
                     'created', 'modified', 'language')
