from django.urls import path

from .views import AssessmentView

app_name = "assessment"

urlpatterns = [
    path("", AssessmentView.as_view(), name="index"),
]
