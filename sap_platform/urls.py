from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from about.views import CareersView
from core.views import robots_txt
from legal.views import LegalPageView
from sap_platform.sitemaps import sitemaps

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("services/", include("services.urls")),
    path("solutions/", include("solutions.urls")),
    path("industries/", include("industries.urls")),
    path("sap-expertise/", include("sap_expertise.urls")),
    path("case-studies/", include("case_studies.urls")),
    path("about/", include("about.urls")),
    path("insights/", include("insights.urls")),
    path("contact/", include("leads.urls")),
    path("assessment/", include("assessment.urls")),
    path("careers/", CareersView.as_view(), name="careers"),
    path("privacy-policy/", LegalPageView.as_view(), {"slug": "privacy-policy"}, name="privacy_policy"),
    path("terms/", LegalPageView.as_view(), {"slug": "terms"}, name="terms"),
    path("cookie-policy/", LegalPageView.as_view(), {"slug": "cookie-policy"}, name="cookie_policy"),
    path("disclaimer/", LegalPageView.as_view(), {"slug": "disclaimer"}, name="disclaimer"),
    path("accessibility/", LegalPageView.as_view(), {"slug": "accessibility"}, name="accessibility"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
]

