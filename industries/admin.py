from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from core.models import FAQ

from .models import Industry, IndustryListItem


class IndustryListItemInline(admin.TabularInline):
    model = IndustryListItem
    extra = 1


class FAQInline(GenericTabularInline):
    model = FAQ
    extra = 1


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("related_services",)
    inlines = [IndustryListItemInline, FAQInline]
