from django.db import models


class TeamMember(models.Model):
    """
    Section 19. No real personnel data is available, and Section 2's
    content-integrity rule prohibits inventing people, expertise, or
    certifications — so this model is intentionally seeded with nothing.
    Real profiles get added via /admin/ once available; until then the team
    page shows the practice's expertise categories instead (see
    about/views.py and templates/about/team.html), the same pattern used in
    Section 7 for capability categories when there are no real client logos.
    """

    SAP_ARCHITECTS = "sap_architects"
    FUNCTIONAL_CONSULTANTS = "functional_consultants"
    TECHNICAL_CONSULTANTS = "technical_consultants"
    INTEGRATION_SPECIALISTS = "integration_specialists"
    ABAP_DEVELOPERS = "abap_developers"
    FIORI_UI5_DEVELOPERS = "fiori_ui5_developers"
    BTP_SPECIALISTS = "btp_specialists"
    DATA_SPECIALISTS = "data_specialists"
    BASIS_INFRASTRUCTURE = "basis_infrastructure"
    QA_TEST = "qa_test"
    PROJECT_MANAGERS = "project_managers"
    BUSINESS_ANALYSTS = "business_analysts"
    CATEGORY_CHOICES = [
        (SAP_ARCHITECTS, "SAP Architects"),
        (FUNCTIONAL_CONSULTANTS, "Functional Consultants"),
        (TECHNICAL_CONSULTANTS, "Technical Consultants"),
        (INTEGRATION_SPECIALISTS, "Integration Specialists"),
        (ABAP_DEVELOPERS, "ABAP Developers"),
        (FIORI_UI5_DEVELOPERS, "Fiori/UI5 Developers"),
        (BTP_SPECIALISTS, "BTP Specialists"),
        (DATA_SPECIALISTS, "Data Specialists"),
        (BASIS_INFRASTRUCTURE, "Basis/Infrastructure"),
        (QA_TEST, "QA/Test"),
        (PROJECT_MANAGERS, "Project Managers"),
        (BUSINESS_ANALYSTS, "Business Analysts"),
    ]

    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    expertise = models.TextField(blank=True)
    modules = models.CharField(max_length=200, blank=True)
    technologies = models.CharField(max_length=200, blank=True)
    industries = models.CharField(max_length=200, blank=True)
    certifications = models.CharField(
        max_length=300, blank=True, help_text="Only list certifications that are actually verified."
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
