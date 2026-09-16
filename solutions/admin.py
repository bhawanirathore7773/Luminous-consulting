from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from core.models import FAQ

from .models import Solution, SolutionListItem


class SolutionListItemInline(admin.TabularInline):
    model = SolutionListItem
    extra = 1


class FAQInline(GenericTabularInline):
    model = FAQ
    extra = 1


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("related_services", "related_solutions")
    inlines = [SolutionListItemInline, FAQInline]
