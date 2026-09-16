from django.urls import path

from .views import CaseStudyDetailView, CaseStudyListView

app_name = "case_studies"

urlpatterns = [
    path("", CaseStudyListView.as_view(), name="list"),
    path("<slug:slug>/", CaseStudyDetailView.as_view(), name="detail"),
]
