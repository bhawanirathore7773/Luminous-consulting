from django.views.generic import TemplateView

from .models import TeamMember

# Section 16's engagement models — described here since the spec doesn't
# call for a standalone page for them.
DELIVERY_MODELS = [
    {"name": "Project-Based Consulting", "description": "a defined scope, timeline, and deliverable."},
    {"name": "Dedicated SAP Team", "description": "a consistent team embedded with yours for a program's duration."},
    {"name": "Staff Augmentation", "description": "specialist capacity added to your own team."},
    {"name": "Advisory & Architecture", "description": "strategic and architectural guidance without full delivery."},
    {"name": "Managed Services", "description": "ongoing operational ownership of your SAP landscape."},
    {"name": "AMS", "description": "structured, ongoing application support."},
    {"name": "Short-Term Specialist Support", "description": "a specific skill for a defined, limited engagement."},
    {"name": "Emergency SAP Intervention", "description": "urgent, focused help for an active production issue."},
]

VALUES = ["Transparency", "Technical rigor", "Business-first thinking", "Long-term partnership"]


class AboutIndexView(TemplateView):
    template_name = "about/about_index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["delivery_models"] = DELIVERY_MODELS
        context["values"] = VALUES
        return context


class CareersView(TemplateView):
    template_name = "about/careers.html"


class TeamView(TemplateView):
    template_name = "about/team.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grouped = []
        for value, label in TeamMember.CATEGORY_CHOICES:
            members = TeamMember.objects.filter(category=value)
            if members.exists():
                grouped.append({"label": label, "members": members})
        context["team_categories"] = grouped
        context["has_team_members"] = TeamMember.objects.exists()
        context["category_choices"] = TeamMember.CATEGORY_CHOICES
        return context
