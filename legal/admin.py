from django.contrib import admin

from .models import LegalPage


@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "last_updated")
