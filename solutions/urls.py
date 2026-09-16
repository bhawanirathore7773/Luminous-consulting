from django.urls import path

from .views import SolutionDetailView, SolutionListView

app_name = "solutions"

urlpatterns = [
    path("", SolutionListView.as_view(), name="list"),
    path("<slug:slug>/", SolutionDetailView.as_view(), name="detail"),
]
