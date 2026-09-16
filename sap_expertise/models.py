from django.db import models


class ExpertiseItem(models.Model):
    """
    Section 13: SAP Platforms / Technologies / Business Applications /
    Functional Areas. Deliberately a single overview page, not individual
    detail pages — the spec defers those ("each technology/module can have
    a dedicated page later").
    """

    PLATFORMS = "platforms"
    TECHNOLOGIES = "technologies"
    BUSINESS_APPLICATIONS = "business_applications"
    FUNCTIONAL_AREAS = "functional_areas"
    CATEGORY_CHOICES = [
        (PLATFORMS, "SAP Platforms"),
        (TECHNOLOGIES, "SAP Technologies"),
        (BUSINESS_APPLICATIONS, "SAP Business Applications"),
        (FUNCTIONAL_AREAS, "SAP Functional Areas"),
    ]

    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return f"{self.get_category_display()}: {self.name}"
