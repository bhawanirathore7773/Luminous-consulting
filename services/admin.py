from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from core.models import FAQ

from .models import Service, ServiceListItem


class ServiceListItemInline(admin.TabularInline):
    model = ServiceListItem
    extra = 1


class FAQInline(GenericTabularInline):
    model = FAQ
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "featured", "order")
    list_filter = ("featured",)
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("related_services",)
    inlines = [ServiceListItemInline, FAQInline]
