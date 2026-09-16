from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "sap_environment", "project_stage", "source", "created_at")
    list_filter = ("sap_environment", "project_stage", "timeline", "source")
    readonly_fields = ("created_at",)
