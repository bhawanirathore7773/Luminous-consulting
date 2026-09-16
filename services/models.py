from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse

from core.models import FAQ


class Service(models.Model):
    """
    One row per page in Section 10's services directory. Every field maps
    directly to a required section of the service detail page template
    (Hero, Business problem, What we solve, Capabilities, Technology,
    Delivery approach, Deliverables, Engagement model, Who it's for, FAQs,
    Related services, CTA).
    """

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    short_summary = models.CharField(
        max_length=200, help_text="One line, shown on cards (homepage, services index, related-services grids)."
    )
    hero_intro = models.TextField(help_text="Supporting paragraph under the H1 on the detail page.")
    business_problem = models.TextField()
    delivery_approach = models.TextField()
    engagement_model = models.TextField(help_text="Which engagement model(s) typically apply, and why.")
    who_its_for = models.TextField()

    cta_label = models.CharField(
        max_length=80,
        default="Talk to an SAP Expert",
        help_text="Section 23: every page should use a contextual CTA, not the same one everywhere.",
    )

    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    featured = models.BooleanField(
        default=False, help_text="Shown in the homepage's 8-category services teaser."
    )
    order = models.PositiveIntegerField(default=0)

    related_services = models.ManyToManyField("self", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    faqs = GenericRelation(FAQ)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("services:detail", kwargs={"slug": self.slug})

    def items(self, section):
        return self.list_items.filter(section=section)

    @property
    def what_we_solve(self):
        return self.items(ServiceListItem.WHAT_WE_SOLVE)

    @property
    def capabilities(self):
        return self.items(ServiceListItem.CAPABILITIES)

    @property
    def technology(self):
        return self.items(ServiceListItem.TECHNOLOGY)

    @property
    def deliverables(self):
        return self.items(ServiceListItem.DELIVERABLES)

    @property
    def display_meta_title(self):
        return self.meta_title or self.name

    @property
    def display_meta_description(self):
        return self.meta_description or self.short_summary


class ServiceListItem(models.Model):
    """
    One bullet point, tagged by which section of the page it belongs to.
    Replaces what would otherwise be four nearly-identical models
    (WhatWeSolveItem, CapabilityItem, TechnologyItem, DeliverableItem).
    """

    WHAT_WE_SOLVE = "what_we_solve"
    CAPABILITIES = "capabilities"
    TECHNOLOGY = "technology"
    DELIVERABLES = "deliverables"
    SECTION_CHOICES = [
        (WHAT_WE_SOLVE, "What we solve"),
        (CAPABILITIES, "Capabilities"),
        (TECHNOLOGY, "Technology"),
        (DELIVERABLES, "Deliverables"),
    ]

    service = models.ForeignKey(Service, related_name="list_items", on_delete=models.CASCADE)
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    text = models.CharField(max_length=300)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["section", "order", "id"]

    def __str__(self):
        return f"{self.get_section_display()}: {self.text}"
