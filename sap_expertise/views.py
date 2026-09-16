from django.views.generic import TemplateView

from .models import ExpertiseItem


class ExpertiseView(TemplateView):
    template_name = "sap_expertise/expertise_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grouped = []
        for value, label in ExpertiseItem.CATEGORY_CHOICES:
            items = ExpertiseItem.objects.filter(category=value)
            if items.exists():
                grouped.append({"label": label, "items": items})
        context["grouped_expertise"] = grouped
        return context
