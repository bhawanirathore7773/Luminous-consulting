from django import forms

from .models import Lead

INPUT_CLASSES = (
    "w-full rounded-md border border-gray-200 px-4 py-2.5 text-sm text-ink "
    "focus:border-accent focus:outline-none"
)


class LeadForm(forms.ModelForm):
    required_services = forms.MultipleChoiceField(
        choices=Lead.SERVICE_CHOICES, required=False, widget=forms.CheckboxSelectMultiple
    )

    # Honeypot: invisible to real visitors (rendered as a hidden input),
    # but bots that fill in every field on a page trip it. No CAPTCHA or JS
    # dependency needed for this level of spam protection.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Lead
        fields = [
            "name",
            "work_email",
            "company",
            "job_title",
            "country",
            "phone",
            "sap_environment",
            "current_sap_system",
            "required_services",
            "project_stage",
            "timeline",
            "estimated_scope",
            "message",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "work_email": forms.EmailInput(attrs={"class": INPUT_CLASSES}),
            "company": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "job_title": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "country": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "phone": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "sap_environment": forms.Select(attrs={"class": INPUT_CLASSES}),
            "current_sap_system": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "project_stage": forms.Select(attrs={"class": INPUT_CLASSES}),
            "timeline": forms.Select(attrs={"class": INPUT_CLASSES}),
            "estimated_scope": forms.Select(attrs={"class": INPUT_CLASSES}),
            "message": forms.Textarea(attrs={"class": INPUT_CLASSES, "rows": 5}),
        }

    def clean_website(self):
        value = self.cleaned_data.get("website")
        if value:
            raise forms.ValidationError("Spam detected.")
        return value

    def clean_required_services(self):
        return ",".join(self.cleaned_data.get("required_services", []))
