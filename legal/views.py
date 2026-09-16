from django.views.generic import DetailView

from .models import LegalPage


class LegalPageView(DetailView):
    model = LegalPage
    template_name = "legal/legal_page.html"
    context_object_name = "page"
    slug_field = "slug"
    slug_url_kwarg = "slug"
