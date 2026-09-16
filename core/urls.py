from django.urls import path

from core.views import ApproachView, HomeView, healthz

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("approach/", ApproachView.as_view(), name="approach"),
    path("healthz/", healthz, name="healthz"),
]
