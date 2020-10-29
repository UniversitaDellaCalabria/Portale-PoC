import nested_admin

from django.contrib import admin

from . models import *


class CarouselItemLinkInline(nested_admin.NestedStackedInline):
    model = CarouselItemLink
    extra = 0
    sortable_field_name = "order"
    classes = ['collapse']


class CarouselItemInline(nested_admin.NestedStackedInline):
    model = CarouselItem
    extra = 0
    inlines = (CarouselItemLinkInline,)
    sortable_field_name = "order"
    classes = ['collapse']


@admin.register(Carousel)
class CarouselAdmin(nested_admin.NestedModelAdmin):
    list_display  = ('name', 'is_active')
    search_fields   = ('name',)
    list_filter = ('created', 'modified')
    inlines = (CarouselItemInline,)
