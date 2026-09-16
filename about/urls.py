from django.urls import path

from .views import AboutIndexView, TeamView

app_name = "about"

urlpatterns = [
    path("", AboutIndexView.as_view(), name="index"),
    path("team/", TeamView.as_view(), name="team"),
]
