import json

from django.conf import settings
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, ListView

from .models import Industry


class IndustryListView(ListView):
    model = Industry
    template_name = "industries/industry_list.html"
    context_object_name = "industries"


class IndustryDetailView(DetailView):
    model = Industry
    template_name = "industries/industry_detail.html"
    context_object_name = "industry"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        industry = self.object
        context["related_services"] = industry.related_services.all()
        context["hero_title"] = f"SAP for {industry.name}"
        context["detail_cta_subtext"] = f"A focused conversation about SAP in {industry.name.lower()}, no obligation."

        schema = {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": f"SAP for {industry.name}",
            "description": industry.display_meta_description,
            "provider": {"@type": "Organization", "name": settings.SITE_NAME},
        }
        context["industry_schema_json"] = mark_safe(
            json.dumps(schema).replace("</script>", "<\\/script>")
        )
        return context
