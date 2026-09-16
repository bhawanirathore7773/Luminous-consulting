import json

from django.conf import settings
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, ListView

from .models import Solution


class SolutionListView(ListView):
    model = Solution
    template_name = "solutions/solution_list.html"
    context_object_name = "solutions"


class SolutionDetailView(DetailView):
    model = Solution
    template_name = "solutions/solution_detail.html"
    context_object_name = "solution"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solution = self.object

        related_solutions = list(solution.related_solutions.all())
        if not related_solutions:
            related_solutions = list(Solution.objects.exclude(pk=solution.pk)[:3])
        context["related_solutions"] = related_solutions
        context["related_services"] = solution.related_services.all()
        context["detail_cta_subtext"] = f"A focused conversation about {solution.name}, no obligation."

        schema = {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": solution.name,
            "description": solution.display_meta_description,
            "provider": {"@type": "Organization", "name": settings.SITE_NAME},
        }
        context["solution_schema_json"] = mark_safe(
            json.dumps(schema).replace("</script>", "<\\/script>")
        )
        return context
