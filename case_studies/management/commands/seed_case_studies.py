"""
Seeds 5 representative SAP use cases (Section 18).

No real client engagements are available, so every entry describes a
business archetype ("a discrete manufacturer") rather than naming a real or
invented company — Section 2's content-integrity rule and Section 18's own
"Representative SAP Use Cases" guidance both call for this.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from case_studies.models import CaseStudy
from industries.models import Industry
from services.models import Service

CASE_STUDIES_DATA = [
    {
        "slug": "s4hana-conversion-discrete-manufacturer",
        "title": "S/4HANA Conversion for a Discrete Manufacturer",
        "short_summary": "A representative brownfield S/4HANA conversion for a mid-size manufacturer with significant custom code.",
        "industry_slug": "manufacturing",
        "business_challenge": "A mid-size discrete manufacturer was running SAP ECC with over a decade of accumulated custom code and was under pressure to move to S/4HANA before mainstream ECC support ended, without disrupting production.",
        "sap_environment": "SAP ECC 6.0, on-premise, with extensive custom ABAP across production planning and quality management.",
        "objective": "Convert to S/4HANA on a realistic timeline while minimizing changes to stable, well-functioning custom logic.",
        "approach": "A phased brownfield conversion, starting with a custom code assessment to separate code that needed remediation from code that could convert cleanly.",
        "solution": "System conversion to S/4HANA with targeted ABAP remediation, followed by a Fiori rollout for shop-floor and quality transactions.",
        "technology_used": "S/4HANA, SAP Readiness Check, SAP Custom Code Migration app, SAP Fiori",
        "outcome": "The organization moved to S/4HANA without a production disruption, with the custom code footprint reduced substantially during the conversion rather than carried forward unchanged.",
        "related_services": ["sap-s4hana", "sap-development"],
        "order": 1,
    },
    {
        "slug": "integration-architecture-regional-retailer",
        "title": "Integration Architecture for a Regional Retail Chain",
        "short_summary": "A representative integration engagement replacing fragile point-to-point interfaces with a governed platform.",
        "industry_slug": "retail-consumer",
        "business_challenge": "A regional retail chain had accumulated a dozen point-to-point integrations between SAP and its e-commerce and POS platforms, with no central monitoring and frequent silent failures.",
        "sap_environment": "SAP S/4HANA with direct point-to-point interfaces to POS and e-commerce systems.",
        "objective": "Replace fragile point-to-point interfaces with a governed, monitored integration layer without disrupting daily store operations.",
        "approach": "Mapped all existing interfaces, prioritized by business risk, and rebuilt them incrementally on SAP BTP Integration Suite with centralized monitoring.",
        "solution": "A consolidated integration layer on SAP BTP Integration Suite, with alerting on failed messages and a documented architecture the internal team could maintain.",
        "technology_used": "SAP BTP Integration Suite, REST/OData APIs",
        "outcome": "Integration failures became visible and actionable within minutes instead of being discovered by store staff, and new integrations could be added against a documented pattern rather than built from scratch.",
        "related_services": ["sap-integration", "sap-btp"],
        "order": 2,
    },
    {
        "slug": "authorization-redesign-financial-services-group",
        "title": "Authorization Redesign for a Financial Services Group",
        "short_summary": "A representative SAP security engagement remediating segregation-of-duties conflicts ahead of an audit.",
        "industry_slug": "banking-financial-services",
        "business_challenge": "An internal audit flagged significant segregation-of-duties conflicts in a financial services group's SAP authorization model, accumulated over years of ad hoc role changes.",
        "sap_environment": "SAP ECC with a role model that had grown organically with no formal segregation-of-duties review process.",
        "objective": "Remediate the flagged conflicts and establish a repeatable process for reviewing future authorization changes.",
        "approach": "Ran a full segregation-of-duties analysis against actual user activity, then redesigned roles in phases to avoid disrupting legitimate day-to-day work.",
        "solution": "A redesigned authorization concept aligned to segregation-of-duties principles, plus a documented change-review process going forward.",
        "technology_used": "SAP GRC Access Control",
        "outcome": "The flagged conflicts were resolved ahead of the follow-up audit, with a documented process in place so new conflicts are caught before go-live rather than during the next audit cycle.",
        "related_services": ["sap-security"],
        "order": 3,
    },
    {
        "slug": "reporting-consolidation-logistics-provider",
        "title": "Reporting Consolidation for a Logistics Provider",
        "short_summary": "A representative data and analytics engagement resolving inconsistent reporting across warehouse and transportation operations.",
        "industry_slug": "logistics-supply-chain",
        "business_challenge": "A logistics provider's warehouse and transportation teams each maintained their own reports, and monthly numbers rarely matched at the executive level.",
        "sap_environment": "SAP EWM and TM, with reporting built ad hoc in spreadsheets pulled from each system separately.",
        "objective": "Establish a single, consistent data model that both operational and executive reporting could draw from.",
        "approach": "Built a consolidated data model spanning EWM and TM before touching any dashboards, so every downstream report would be consistent by construction.",
        "solution": "A unified data model in SAP Datasphere feeding both operational dashboards and executive reporting.",
        "technology_used": "SAP Datasphere, SAP Analytics Cloud",
        "outcome": "Warehouse and transportation numbers reconciled automatically for the first time, removing a recurring monthly exercise of manually explaining discrepancies.",
        "related_services": ["sap-data-analytics", "sap-integration"],
        "order": 4,
    },
    {
        "slug": "btp-extension-professional-services-firm",
        "title": "BTP Extension for a Professional Services Firm",
        "short_summary": "A representative SAP BTP engagement automating utilization reporting without modifying the core system.",
        "industry_slug": "professional-services",
        "business_challenge": "A professional services firm needed real-time utilization and margin visibility that standard SAP reporting couldn't provide, but wanted to avoid custom ABAP in the core system.",
        "sap_environment": "SAP S/4HANA with project systems and controlling, no existing BTP footprint.",
        "objective": "Deliver real-time utilization and margin reporting without adding custom logic to the core SAP system.",
        "approach": "Built the reporting logic entirely on SAP BTP, keeping the core S/4HANA system unmodified and upgrade-safe.",
        "solution": "A BTP-based application pulling project and time data into a real-time utilization and margin dashboard.",
        "technology_used": "SAP BTP (Cloud Foundry), CAP, SAP Analytics Cloud",
        "outcome": "Practice leads could see engagement-level margin in near real time instead of waiting for month-end close, with zero custom code added to the core SAP system.",
        "related_services": ["sap-btp", "sap-data-analytics"],
        "order": 5,
    },
]


class Command(BaseCommand):
    help = "Seeds 5 representative SAP use cases (Section 18)."

    @transaction.atomic
    def handle(self, *args, **options):
        for data in CASE_STUDIES_DATA:
            industry = Industry.objects.filter(slug=data["industry_slug"]).first()
            case_study, created = CaseStudy.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "title": data["title"],
                    "short_summary": data["short_summary"],
                    "industry": industry,
                    "business_challenge": data["business_challenge"],
                    "sap_environment": data["sap_environment"],
                    "objective": data["objective"],
                    "approach": data["approach"],
                    "solution": data["solution"],
                    "technology_used": data["technology_used"],
                    "outcome": data["outcome"],
                    "order": data["order"],
                },
            )
            related = Service.objects.filter(slug__in=data["related_services"])
            case_study.related_services.set(related)
            self.stdout.write(f"{'Created' if created else 'Updated'} case study: {case_study.title}")

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(CASE_STUDIES_DATA)} case studies."))
