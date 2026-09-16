from django.contrib import admin

from .models import ExpertiseItem


@admin.register(ExpertiseItem)
class ExpertiseItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order")
    list_filter = ("category",)
