from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView

from case_studies.models import CaseStudy
from industries.models import Industry
from services.models import Service

OUTCOME_PILLARS = [
    {"name": "Modernize", "description": "Modernize legacy SAP landscapes."},
    {"name": "Integrate", "description": "Connect SAP with the wider enterprise ecosystem."},
    {"name": "Optimize", "description": "Improve business processes and system performance."},
    {"name": "Scale", "description": "Build scalable enterprise architecture."},
    {"name": "Operate", "description": "Keep SAP reliable through structured support and managed services."},
    {"name": "Innovate", "description": "Use BTP, data, automation, and AI where they create measurable value."},
]

CAPABILITY_CATEGORIES = [
    "SAP Advisory",
    "Implementation",
    "Integration",
    "Development",
    "Migration",
    "Managed Services",
]

PROBLEM_TO_SERVICE = [
    {"problem": "Modernize SAP", "service": "SAP Advisory & Strategy", "url": "/services/sap-consulting/"},
    {"problem": "Migrate to S/4HANA", "service": "SAP S/4HANA", "url": "/services/sap-s4hana/"},
    {"problem": "Integrate SAP", "service": "SAP Integration", "url": "/services/sap-integration/"},
    {"problem": "Improve performance", "service": "SAP AMS & Managed Services", "url": "/services/sap-ams/"},
    {"problem": "Reduce support backlog", "service": "SAP AMS & Managed Services", "url": "/services/sap-ams/"},
    {"problem": "Build SAP extensions", "service": "SAP BTP", "url": "/services/sap-btp/"},
    {"problem": "Improve reporting", "service": "SAP Data, Analytics & AI", "url": "/services/sap-data-analytics/"},
    {"problem": "Strengthen security", "service": "SAP Development", "url": "/services/sap-development/"},
    {"problem": "Need SAP expertise", "service": "SAP Advisory & Strategy", "url": "/services/sap-consulting/"},
    {"problem": "Not sure", "service": "Talk to an SAP Expert", "url": "/contact/"},
]

PUBLIC_CUSTOMER_STORIES = [
    {
        "mark": "SC",
        "company": "Samsung C&T",
        "industry": "Construction",
        "title": "S/4HANA + BTP for construction",
        "summary": "A public SAP story covering S/4HANA Cloud Private Edition, SAP BTP and Integration Suite for a complex global construction landscape.",
        "url": "https://www.sap.com/asset/dynamic/2025/06/ce5ba95c-0a7f-0010-bca6-c68f7e60039b.html",
    },
    {
        "mark": "SE",
        "company": "Schneider Electric",
        "industry": "Manufacturing",
        "title": "Cloud-native transport planning",
        "summary": "A public 2026 SAP Innovation Awards story using BTP, Datasphere, CAP, Fiori and event-driven services while keeping the S/4HANA core clean.",
        "url": "https://www.sap.com/documents/2026/02/ca37ea09-3f7f-0010-bca6-c68f7e60039b.html",
    },
    {
        "mark": "VH",
        "company": "Vorwerk",
        "industry": "Retail",
        "title": "Digital direct-sales experience",
        "summary": "A public SAP story using BTP and Integration Suite to connect a digital sales solution with SAP and third-party back-end systems.",
        "url": "https://www.sap.com/netherlands/asset/dynamic/2024/11/d8b472ef-e17e-0010-bca6-c68f7e60039b.html",
    },
    {
        "mark": "HC",
        "company": "The Hershey Company",
        "industry": "Consumer products",
        "title": "Data, analytics and clean core",
        "summary": "A public SAP story combining S/4HANA, BTP, Datasphere and Analytics Cloud to make enterprise data easier to access and trust.",
        "url": "https://www.sap.com/netherlands/asset/dynamic/2024/09/44538d45-d57e-0010-bca6-c68f7e60039b.html",
    },
    {
        "mark": "DA",
        "company": "Daikin Industries",
        "industry": "Manufacturing",
        "title": "AI-powered forecasting",
        "summary": "A public 2026 SAP Innovation Awards story using BTP and AI to improve forecasting across a large branch network.",
        "url": "https://www.sap.com/documents/2026/03/5047963c-437f-0010-bca6-c68f7e60039b.html",
    },
    {
        "mark": "SS",
        "company": "Sasol",
        "industry": "Logistics",
        "title": "Modern transportation management",
        "summary": "A public SAP Innovation Awards story covering S/4HANA Supply Chain, BTP and logistics integration for transportation planning and execution.",
        "url": "https://www.sap.com/documents/2026/03/a007e64f-437f-0010-bca6-c68f7e60039b.html",
    },
]

PUBLIC_CUSTOMER_VOICES = [
    {
        "quote": "SAP BTP and SAP Integration Suite enabled a digital solution connected to SAP and third-party systems.",
        "person": "Adnan Gusinjac",
        "company": "Vorwerk Group",
        "url": "https://www.sap.com/netherlands/asset/dynamic/2024/11/d8b472ef-e17e-0010-bca6-c68f7e60039b.html",
    },
    {
        "quote": "SAP Integration Suite helped connect systems efficiently and support real-time decision-making.",
        "person": "Hyo-Seung Nam",
        "company": "Samsung C&T Corporation",
        "url": "https://www.sap.com/asset/dynamic/2025/06/ce5ba95c-0a7f-0010-bca6-c68f7e60039b.html",
    },
]



def _stack_layer(label, index, emphasis):
    y = 8 + index * 68
    if emphasis:
        fill, stroke, text_color = (
            "rgb(var(--color-navy-950))",
            "rgb(var(--color-navy-950))",
            "#FFFFFF",
        )
    else:
        fill, stroke, text_color = (
            "rgb(var(--color-gray-50))",
            "rgb(var(--color-gray-200))",
            "rgb(var(--color-ink))",
        )
    return {
        "label": label,
        "y": y,
        "text_y": y + 27,
        "fill": fill,
        "stroke": stroke,
        "text_color": text_color,
    }


HERO_STACK = [
    _stack_layer("Business Processes", 0, emphasis=False),
    _stack_layer("SAP Core", 1, emphasis=True),
    _stack_layer("S/4HANA", 2, emphasis=True),
    _stack_layer("SAP BTP", 3, emphasis=True),
    _stack_layer("Integration", 4, emphasis=False),
    _stack_layer("Data & Analytics", 5, emphasis=False),
    _stack_layer("Automation / AI", 6, emphasis=False),
]


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = Service.objects.filter(featured=True)[:8]
        context["industries"] = Industry.objects.all()[:6]
        context["case_studies"] = CaseStudy.objects.all()[:3]
        context["outcomes"] = OUTCOME_PILLARS
        context["capabilities"] = CAPABILITY_CATEGORIES
        context["problem_options"] = PROBLEM_TO_SERVICE
        context["hero_stack"] = HERO_STACK
        context["public_customer_stories"] = PUBLIC_CUSTOMER_STORIES
        context["public_customer_voices"] = PUBLIC_CUSTOMER_VOICES
        return context


METHODOLOGY_STEPS = [
    {"number": "01", "name": "Discover", "items": ["Business objectives", "Current landscape", "Pain points"]},
    {"number": "02", "name": "Assess", "items": ["Processes", "Architecture", "Data", "Integration", "Technical debt"]},
    {"number": "03", "name": "Design", "items": ["Target architecture", "Roadmap", "Solution design", "Delivery plan"]},
    {"number": "04", "name": "Deliver", "items": ["Configure", "Develop", "Integrate", "Migrate", "Test", "Deploy"]},
    {"number": "05", "name": "Stabilize", "items": ["Go-live", "Hypercare", "Issue resolution", "Knowledge transfer"]},
    {"number": "06", "name": "Optimize", "items": ["Performance", "Automation", "Enhancements", "Continuous improvement"]},
]


class ApproachView(TemplateView):
    template_name = "core/approach.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["methodology_steps"] = METHODOLOGY_STEPS
        return context


def healthz(request):
    """Lightweight readiness endpoint for Render/nginx health checks."""
    try:
        connection.ensure_connection()
    except Exception:
        return JsonResponse({"status": "unhealthy"}, status=503)
    return JsonResponse({"status": "ok"})


def robots_txt(request):
    sitemap_url = request.build_absolute_uri("/sitemap.xml")
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /contact/thank-you/",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
