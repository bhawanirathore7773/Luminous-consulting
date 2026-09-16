from django.views.generic import DetailView, ListView

from .models import CaseStudy


class CaseStudyListView(ListView):
    model = CaseStudy
    template_name = "case_studies/case_study_list.html"
    context_object_name = "case_studies"


class CaseStudyDetailView(DetailView):
    model = CaseStudy
    template_name = "case_studies/case_study_detail.html"
    context_object_name = "case_study"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        case_study = self.object
        context["related_services"] = case_study.related_services.all()
        context["detail_cta_subtext"] = "A focused conversation about a challenge like this one, no obligation."
        return context
