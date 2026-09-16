from django.urls import path

from .views import ContactView, ThankYouView

app_name = "leads"

urlpatterns = [
    path("", ContactView.as_view(), name="contact"),
    path("thank-you/", ThankYouView.as_view(), name="thank_you"),
]
