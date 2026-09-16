"""
Site-wide navigation, footer, and CTA data.

Phase 1 keeps this as plain Python data so the header/footer/mega-menus are
fully wired and stylable before the Service/Solution/Industry models exist.
When those apps land (Phases 2–4), replace the hardcoded lists below with
querysets — the templates already loop over this shape, so no template
changes are needed at that point.
"""

from django.conf import settings

PRIMARY_CTA = {"label": "Talk to an SAP Expert", "url": "/contact/"}

PRIMARY_NAV = [
    {"label": "Services", "url": "/services/", "megamenu": "services"},
    {"label": "Solutions", "url": "/solutions/", "megamenu": "solutions"},
    {"label": "Industries", "url": "/industries/", "megamenu": "industries"},
    {"label": "SAP Expertise", "url": "/sap-expertise/", "megamenu": None},
    {"label": "Approach", "url": "/approach/", "megamenu": None},
    {"label": "Insights", "url": "/insights/", "megamenu": None},
    {"label": "About", "url": "/about/", "megamenu": None},
]

MEGA_MENUS = {
    "services": [
        {"label": "SAP Consulting", "url": "/services/sap-consulting/"},
        {"label": "S/4HANA", "url": "/services/sap-s4hana/"},
        {"label": "Implementation", "url": "/services/sap-implementation/"},
        {"label": "Migration", "url": "/services/sap-migration/"},
        {"label": "Integration", "url": "/services/sap-integration/"},
        {"label": "BTP", "url": "/services/sap-btp/"},
        {"label": "Development", "url": "/services/sap-development/"},
        {"label": "Data & Analytics", "url": "/services/sap-data-analytics/"},
        {"label": "Security", "url": "/services/sap-security/"},
        {"label": "Testing", "url": "/services/sap-testing/"},
        {"label": "AMS", "url": "/services/sap-ams/"},
        {"label": "Managed Services", "url": "/services/sap-managed-services/"},
    ],
    "solutions": [
        {"label": "SAP Transformation", "url": "/solutions/sap-transformation/"},
        {"label": "SAP Modernization", "url": "/solutions/sap-modernization/"},
        {"label": "Cloud", "url": "/solutions/cloud-transformation/"},
        {"label": "Integration", "url": "/solutions/sap-integration/"},
        {"label": "Automation", "url": "/solutions/automation/"},
        {"label": "Data & AI", "url": "/solutions/data-ai/"},
    ],
    "industries": [
        {"label": "Manufacturing", "url": "/industries/manufacturing/"},
        {"label": "Automotive", "url": "/industries/automotive/"},
        {"label": "Pharma & Life Sciences", "url": "/industries/pharma-life-sciences/"},
        {"label": "Retail & Consumer", "url": "/industries/retail-consumer/"},
        {"label": "Logistics", "url": "/industries/logistics-supply-chain/"},
        {"label": "Energy & Utilities", "url": "/industries/energy-utilities/"},
        {"label": "Engineering & Construction", "url": "/industries/engineering-construction/"},
        {"label": "Professional Services", "url": "/industries/professional-services/"},
    ],
}

FOOTER_COLUMNS = [
    {
        "heading": "Company",
        "links": [
            {"label": "About", "url": "/about/"},
            {"label": "Team", "url": "/about/team/"},
            {"label": "Careers", "url": "/careers/"},
            {"label": "Contact", "url": "/contact/"},
        ],
    },
    {
        "heading": "Services",
        "links": [
            {"label": "Consulting", "url": "/services/sap-consulting/"},
            {"label": "S/4HANA", "url": "/services/sap-s4hana/"},
            {"label": "Implementation", "url": "/services/sap-implementation/"},
            {"label": "Integration", "url": "/services/sap-integration/"},
            {"label": "BTP", "url": "/services/sap-btp/"},
            {"label": "AMS & Support", "url": "/services/sap-ams/"},
        ],
    },
    {
        "heading": "Industries",
        "links": [
            {"label": "Manufacturing", "url": "/industries/manufacturing/"},
            {"label": "Automotive", "url": "/industries/automotive/"},
            {"label": "Pharma & Life Sciences", "url": "/industries/pharma-life-sciences/"},
            {"label": "Retail & Consumer", "url": "/industries/retail-consumer/"},
            {"label": "Energy & Utilities", "url": "/industries/energy-utilities/"},
        ],
    },
    {
        "heading": "Resources",
        "links": [
            {"label": "SAP Expertise", "url": "/sap-expertise/"},
            {"label": "Insights", "url": "/insights/"},
            {"label": "Case Studies", "url": "/case-studies/"},
        ],
    },
    {
        "heading": "Legal",
        "links": [
            {"label": "Privacy Policy", "url": "/privacy-policy/"},
            {"label": "Terms", "url": "/terms/"},
            {"label": "Cookie Policy", "url": "/cookie-policy/"},
            {"label": "Accessibility", "url": "/accessibility/"},
            {"label": "Disclaimer", "url": "/disclaimer/"},
        ],
    },
]


def global_nav(request):
    return {
        "site_name": settings.SITE_NAME,
        "primary_cta": PRIMARY_CTA,
        "primary_nav": PRIMARY_NAV,
        "mega_menus": MEGA_MENUS,
        "footer_columns": FOOTER_COLUMNS,
    }
