import json

from django.conf import settings
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, ListView

from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "insights/insight_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        queryset = Article.objects.all()
        query = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category", "").strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(summary__icontains=query) | Q(content__icontains=query)
            )
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        context["selected_category"] = self.request.GET.get("category", "")
        context["categories"] = Article.CATEGORY_CHOICES
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = "insights/insight_detail.html"
    context_object_name = "article"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object

        related_articles = list(article.related_articles.all())
        if not related_articles:
            related_articles = list(
                Article.objects.filter(category=article.category).exclude(pk=article.pk)[:3]
            )
        context["related_articles"] = related_articles
        context["related_services"] = article.related_services.all()

        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": article.title,
            "description": article.display_meta_description,
            # Organization, not Person — no real named author is on file.
            "author": {"@type": "Organization", "name": article.author},
            "datePublished": article.published_date.isoformat(),
            "publisher": {"@type": "Organization", "name": settings.SITE_NAME},
        }
        context["article_schema_json"] = mark_safe(
            json.dumps(schema).replace("</script>", "<\\/script>")
        )
        return context
