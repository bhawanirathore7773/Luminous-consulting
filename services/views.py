import json

from django.conf import settings
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, ListView

from .models import Service


class ServiceListView(ListView):
    model = Service
    template_name = "services/service_list.html"
    context_object_name = "services"


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/service_detail.html"
    context_object_name = "service"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.object

        related = list(service.related_services.all())
        if not related:
            related = list(Service.objects.exclude(pk=service.pk)[:3])
        context["related_services"] = related

        context["detail_cta_subtext"] = f"A focused conversation about {service.name}, no obligation."

        schema = {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": service.name,
            "description": service.display_meta_description,
            "provider": {"@type": "Organization", "name": settings.SITE_NAME},
        }
        # Defense-in-depth: a stray "</script>" in admin-entered content
        # shouldn't be able to break out of the schema <script> tag.
        context["service_schema_json"] = mark_safe(
            json.dumps(schema).replace("</script>", "<\\/script>")
        )
        return context
