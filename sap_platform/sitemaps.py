from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from case_studies.models import CaseStudy
from industries.models import Industry
from insights.models import Article
from legal.models import LegalPage
from services.models import Service
from solutions.models import Solution


class StaticViewSitemap(Sitemap):
    """Pages with no dedicated model: home, section indexes, and the
    standalone pages built across the phases (approach, careers, contact,
    assessment)."""

    changefreq = "monthly"

    def items(self):
        return [
            "core:home",
            "core:approach",
            "services:list",
            "solutions:list",
            "industries:list",
            "sap_expertise:index",
            "case_studies:list",
            "insights:list",
            "about:index",
            "about:team",
            "careers",
            "leads:contact",
            "assessment:index",
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == "core:home" else 0.6


class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Service.objects.all()


class SolutionSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Solution.objects.all()


class IndustrySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Industry.objects.all()


class CaseStudySitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return CaseStudy.objects.all()


class ArticleSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def lastmod(self, obj):
        return obj.updated_at

    def items(self):
        return Article.objects.all()


class LegalPageSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.3

    def lastmod(self, obj):
        return obj.last_updated

    def items(self):
        return LegalPage.objects.all()

    def location(self, obj):
        return f"/{obj.slug}/"


sitemaps = {
    "static": StaticViewSitemap,
    "services": ServiceSitemap,
    "solutions": SolutionSitemap,
    "industries": IndustrySitemap,
    "case_studies": CaseStudySitemap,
    "insights": ArticleSitemap,
    "legal": LegalPageSitemap,
}
