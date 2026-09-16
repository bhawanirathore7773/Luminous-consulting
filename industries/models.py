from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse

from core.models import FAQ


class Industry(models.Model):
    """
    One row per page in Section 12. The required blocks are: Industry
    challenges, Business processes, SAP landscape, Relevant SAP modules,
    Integration requirements, Transformation opportunities, Typical use
    cases, Services, Outcomes, FAQs, CTA — that's 11, matched 1:1 below
    (six as IndustryListItem sections, sap_landscape/outcomes as paragraphs,
    Services via the related_services M2M, FAQs generic, CTA via cta_label).
    """

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    short_summary = models.CharField(max_length=200)
    hero_intro = models.TextField()

    sap_landscape = models.TextField(help_text="What SAP and adjacent systems typically look like in this industry today.")
    outcomes = models.TextField(help_text="Which sitewide outcome pillars apply here, and why.")

    cta_label = models.CharField(max_length=80, default="Discuss Your Industry Challenge")
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    order = models.PositiveIntegerField(default=0)

    related_services = models.ManyToManyField("services.Service", blank=True, related_name="industries")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    faqs = GenericRelation(FAQ)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Industries"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("industries:detail", kwargs={"slug": self.slug})

    def items(self, section):
        return self.list_items.filter(section=section)

    @property
    def challenges(self):
        return self.items(IndustryListItem.CHALLENGES)

    @property
    def business_processes(self):
        return self.items(IndustryListItem.PROCESSES)

    @property
    def relevant_modules(self):
        return self.items(IndustryListItem.MODULES)

    @property
    def integration_requirements(self):
        return self.items(IndustryListItem.INTEGRATION)

    @property
    def transformation_opportunities(self):
        return self.items(IndustryListItem.OPPORTUNITIES)

    @property
    def typical_use_cases(self):
        return self.items(IndustryListItem.USE_CASES)

    @property
    def display_meta_title(self):
        return self.meta_title or self.name

    @property
    def display_meta_description(self):
        return self.meta_description or self.short_summary


class IndustryListItem(models.Model):
    CHALLENGES = "challenges"
    PROCESSES = "processes"
    MODULES = "modules"
    INTEGRATION = "integration_requirements"
    OPPORTUNITIES = "transformation_opportunities"
    USE_CASES = "typical_use_cases"
    SECTION_CHOICES = [
        (CHALLENGES, "Industry challenges"),
        (PROCESSES, "Business processes"),
        (MODULES, "Relevant SAP modules"),
        (INTEGRATION, "Integration requirements"),
        (OPPORTUNITIES, "Transformation opportunities"),
        (USE_CASES, "Typical use cases"),
    ]

    industry = models.ForeignKey(Industry, related_name="list_items", on_delete=models.CASCADE)
    section = models.CharField(max_length=40, choices=SECTION_CHOICES)
    text = models.CharField(max_length=300)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["section", "order", "id"]

    def __str__(self):
        return f"{self.get_section_display()}: {self.text}"
