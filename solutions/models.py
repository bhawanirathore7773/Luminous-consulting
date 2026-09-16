from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse

from core.models import FAQ


class Solution(models.Model):
    """
    Section 11's distinction: SERVICES = what we do, SOLUTIONS = the business
    problem we solve, INDUSTRIES = where we apply it. A solution typically
    bundles several services together (e.g. "SAP Transformation" = Advisory
    + S/4HANA + Integration + Testing delivered as one program).
    """

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    short_summary = models.CharField(max_length=200)
    hero_intro = models.TextField()
    business_problem = models.TextField()
    approach = models.TextField()
    who_its_for = models.TextField()
    cta_label = models.CharField(max_length=80, default="Talk to an SAP Expert")

    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    order = models.PositiveIntegerField(default=0)

    related_services = models.ManyToManyField("services.Service", blank=True, related_name="solutions")
    related_solutions = models.ManyToManyField("self", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    faqs = GenericRelation(FAQ)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("solutions:detail", kwargs={"slug": self.slug})

    def items(self, section):
        return self.list_items.filter(section=section)

    @property
    def what_this_includes(self):
        return self.items(SolutionListItem.WHAT_THIS_INCLUDES)

    @property
    def outcomes_addressed(self):
        return self.items(SolutionListItem.OUTCOMES)

    @property
    def display_meta_title(self):
        return self.meta_title or self.name

    @property
    def display_meta_description(self):
        return self.meta_description or self.short_summary


class SolutionListItem(models.Model):
    WHAT_THIS_INCLUDES = "what_this_includes"
    OUTCOMES = "outcomes"
    SECTION_CHOICES = [
        (WHAT_THIS_INCLUDES, "What this includes"),
        (OUTCOMES, "Outcomes addressed"),
    ]

    solution = models.ForeignKey(Solution, related_name="list_items", on_delete=models.CASCADE)
    section = models.CharField(max_length=30, choices=SECTION_CHOICES)
    text = models.CharField(max_length=300)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["section", "order", "id"]

    def __str__(self):
        return f"{self.get_section_display()}: {self.text}"
