from django.db import models
from django.urls import reverse
from django.utils import timezone


class Article(models.Model):
    """
    Section 21's Insights / Knowledge Center. `author` intentionally
    defaults to an institutional byline rather than an invented named
    individual — no real authors are on file yet, and inventing one would
    be the same fabricated-credibility problem the (empty) team page in
    Phase 4 avoids. `reading_time_minutes` is computed from word count
    rather than stored, so it can't drift out of sync with the content.
    """

    S4HANA = "s4hana"
    BTP = "btp"
    INTEGRATION = "integration"
    SECURITY = "security"
    FINANCE = "finance"
    SUPPLY_CHAIN = "supply_chain"
    MANUFACTURING = "manufacturing"
    DATA_ANALYTICS = "data_analytics"
    AI = "ai"
    AMS = "ams"
    TRANSFORMATION = "transformation"
    CATEGORY_CHOICES = [
        (S4HANA, "S/4HANA"),
        (BTP, "SAP BTP"),
        (INTEGRATION, "Integration"),
        (SECURITY, "SAP Security"),
        (FINANCE, "Finance"),
        (SUPPLY_CHAIN, "Supply Chain"),
        (MANUFACTURING, "Manufacturing"),
        (DATA_ANALYTICS, "Data & Analytics"),
        (AI, "AI"),
        (AMS, "AMS"),
        (TRANSFORMATION, "SAP Transformation"),
    ]

    ARTICLE = "article"
    GUIDE = "guide"
    CHECKLIST = "checklist"
    WHITEPAPER = "whitepaper"
    IMPLEMENTATION_GUIDE = "implementation_guide"
    MIGRATION_GUIDE = "migration_guide"
    ARCHITECTURE_INSIGHT = "architecture_insight"
    CONTENT_TYPE_CHOICES = [
        (ARTICLE, "Article"),
        (GUIDE, "Guide"),
        (CHECKLIST, "Checklist"),
        (WHITEPAPER, "Whitepaper"),
        (IMPLEMENTATION_GUIDE, "Implementation Guide"),
        (MIGRATION_GUIDE, "Migration Guide"),
        (ARCHITECTURE_INSIGHT, "Architecture Insight"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    summary = models.CharField(max_length=250)
    author = models.CharField(max_length=120, default="SAP Practice Team")
    published_date = models.DateField(default=timezone.now)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    content_type = models.CharField(max_length=30, choices=CONTENT_TYPE_CHOICES, default=ARTICLE)
    content = models.TextField()

    related_services = models.ManyToManyField("services.Service", blank=True, related_name="articles")
    related_articles = models.ManyToManyField("self", blank=True)

    cta_label = models.CharField(max_length=80, default="Talk to an SAP Expert")
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_date", "order"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("insights:detail", kwargs={"slug": self.slug})

    @property
    def name(self):
        # Lets Article slot into the generic related_grid.html partial.
        return self.title

    @property
    def short_summary(self):
        return self.summary

    @property
    def reading_time_minutes(self):
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))

    @property
    def display_meta_title(self):
        return self.meta_title or self.title

    @property
    def display_meta_description(self):
        return self.meta_description or self.summary
