from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "content_type", "published_date")
    list_filter = ("category", "content_type")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("related_services", "related_articles")
