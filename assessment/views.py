from django.views.generic import TemplateView


class AssessmentView(TemplateView):
    template_name = "assessment/assessment.html"
