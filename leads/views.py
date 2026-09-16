from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import LeadForm


class ContactView(FormView):
    template_name = "leads/contact.html"
    form_class = LeadForm
    success_url = reverse_lazy("leads:thank_you")

    def get_initial(self):
        initial = super().get_initial()
        summary = self.request.GET.get("summary", "").strip()
        if summary:
            initial["message"] = summary
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["from_assessment"] = self.request.GET.get("source") == "assessment"
        return context

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.source = self.request.GET.get("source", "contact_page")
        lead.save()
        return super().form_valid(form)


class ThankYouView(TemplateView):
    template_name = "leads/thank_you.html"
