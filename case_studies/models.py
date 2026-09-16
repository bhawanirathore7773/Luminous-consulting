from django.db import models
from django.urls import reverse


class CaseStudy(models.Model):
    """
    Section 18's format: Industry, Business challenge, SAP environment,
    Objective, Approach, Solution, Services, Technology, Outcome.

    No real client engagements are available, so every entry here is a
    representative scenario — `title` must describe a business archetype
    ("S/4HANA Conversion for a Discrete Manufacturer"), never a real or
    invented company name, per Section 2's content-integrity rule and
    Section 18's own guidance to label these clearly rather than pretend
    they're real client disclosures.
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    short_summary = models.CharField(max_length=200, help_text="One line for the case-study grid card.")

    industry = models.ForeignKey(
        "industries.Industry", on_delete=models.SET_NULL, null=True, blank=True, related_name="case_studies"
    )
    business_challenge = models.TextField()
    sap_environment = models.CharField(max_length=200, help_text="The landscape before this engagement.")
    objective = models.TextField()
    approach = models.TextField()
    solution = models.TextField()
    technology_used = models.CharField(max_length=300)
    outcome = models.TextField()

    related_services = models.ManyToManyField("services.Service", blank=True, related_name="case_studies")

    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name_plural = "Case studies"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("case_studies:detail", kwargs={"slug": self.slug})

    @property
    def name(self):
        # Lets CaseStudy slot into the generic related_grid.html partial
        # (which expects .name/.short_summary/.get_absolute_url) without a
        # dedicated card template.
        return self.title

    @property
    def display_meta_title(self):
        return self.meta_title or self.title

    @property
    def display_meta_description(self):
        return self.meta_description or self.short_summary
