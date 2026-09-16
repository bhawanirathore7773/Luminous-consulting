from django.urls import path

from .views import ExpertiseView

app_name = "sap_expertise"

urlpatterns = [
    path("", ExpertiseView.as_view(), name="index"),
]
