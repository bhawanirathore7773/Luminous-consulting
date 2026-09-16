from django.contrib import admin

from .models import CaseStudy


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("title", "industry", "order")
    list_filter = ("industry",)
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("related_services",)
