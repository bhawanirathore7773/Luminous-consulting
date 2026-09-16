from django.urls import path

from .views import ArticleDetailView, ArticleListView

app_name = "insights"

urlpatterns = [
    path("", ArticleListView.as_view(), name="list"),
    path("<slug:slug>/", ArticleDetailView.as_view(), name="detail"),
]
