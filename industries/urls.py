from django.urls import path

from .views import IndustryDetailView, IndustryListView

app_name = "industries"

urlpatterns = [
    path("", IndustryListView.as_view(), name="list"),
    path("<slug:slug>/", IndustryDetailView.as_view(), name="detail"),
]
