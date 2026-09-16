from django.db import models


class Lead(models.Model):
    """Section 22's contact/lead-generation form field list, stored as-is."""

    ECC = "ecc"
    S4HANA = "s4hana"
    CLOUD_ERP = "cloud_erp"
    BTP = "btp"
    SUCCESSFACTORS = "successfactors"
    ARIBA = "ariba"
    OTHER_ENV = "other"
    NOT_SURE_ENV = "not_sure"
    SAP_ENVIRONMENT_CHOICES = [
        (ECC, "ECC"),
        (S4HANA, "S/4HANA"),
        (CLOUD_ERP, "SAP Cloud ERP"),
        (BTP, "BTP"),
        (SUCCESSFACTORS, "SuccessFactors"),
        (ARIBA, "Ariba"),
        (OTHER_ENV, "Other"),
        (NOT_SURE_ENV, "Not sure"),
    ]

    SERVICE_CHOICES = [
        ("consulting", "Consulting"),
        ("implementation", "Implementation"),
        ("migration", "Migration"),
        ("integration", "Integration"),
        ("development", "Development"),
        ("ams", "AMS"),
        ("support", "Support"),
        ("btp", "BTP"),
        ("data_analytics", "Data & Analytics"),
        ("security", "Security"),
        ("testing", "Testing"),
        ("other", "Other"),
    ]

    EVALUATING = "evaluating"
    PLANNING = "planning"
    READY_TO_START = "ready_to_start"
    IN_PROGRESS = "in_progress"
    PROJECT_STAGE_CHOICES = [
        (EVALUATING, "Evaluating options"),
        (PLANNING, "Planning"),
        (READY_TO_START, "Ready to start"),
        (IN_PROGRESS, "Already in progress"),
    ]

    IMMEDIATE = "immediate"
    WITHIN_3_MONTHS = "within_3_months"
    THREE_TO_SIX_MONTHS = "3_6_months"
    SIX_TO_TWELVE_MONTHS = "6_12_months"
    TWELVE_PLUS_MONTHS = "12_plus_months"
    TIMELINE_CHOICES = [
        (IMMEDIATE, "Immediate"),
        (WITHIN_3_MONTHS, "Within 3 months"),
        (THREE_TO_SIX_MONTHS, "3–6 months"),
        (SIX_TO_TWELVE_MONTHS, "6–12 months"),
        (TWELVE_PLUS_MONTHS, "12+ months"),
    ]

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    NOT_SURE_SCOPE = "not_sure"
    SCOPE_CHOICES = [
        (SMALL, "Small — single process or module"),
        (MEDIUM, "Medium — multi-module or departmental"),
        (LARGE, "Large — enterprise-wide"),
        (NOT_SURE_SCOPE, "Not sure yet"),
    ]

    name = models.CharField(max_length=120)
    work_email = models.EmailField()
    company = models.CharField(max_length=150)
    job_title = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=40, blank=True)

    sap_environment = models.CharField(max_length=20, choices=SAP_ENVIRONMENT_CHOICES, blank=True)
    current_sap_system = models.CharField(
        max_length=200, blank=True, help_text="Free text — e.g. version, hosting model."
    )
    required_services = models.CharField(max_length=300, blank=True, help_text="Comma-separated service keys.")
    project_stage = models.CharField(max_length=20, choices=PROJECT_STAGE_CHOICES, blank=True)
    timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES, blank=True)
    estimated_scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, blank=True)
    message = models.TextField(blank=True)

    # Section 33: track which page/flow generated the lead (e.g. "contact_page",
    # "assessment") without needing a full analytics platform wired up yet.
    source = models.CharField(max_length=50, default="contact_page")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.company})"

    def required_services_list(self):
        keys = [k.strip() for k in self.required_services.split(",") if k.strip()]
        labels = dict(self.SERVICE_CHOICES)
        return [labels.get(k, k) for k in keys]
