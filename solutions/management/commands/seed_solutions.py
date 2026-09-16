"""
Seeds the 6 solution pages listed in Section 11 of the build spec.

Solutions are framed around the business outcome (Section 11: SERVICES =
what we do, SOLUTIONS = the business problem we solve), and cross-link to
the Service objects that actually deliver them.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import FAQ
from services.models import Service
from solutions.models import Solution, SolutionListItem

SOLUTIONS_DATA = [
    {
        "slug": "sap-transformation",
        "name": "SAP Transformation",
        "short_summary": "End-to-end transformation of your SAP landscape — from strategy through to stabilized operations.",
        "hero_intro": "SAP transformation programs touch process, technology, and people at once — the risk isn't any single workstream, it's how they interact.",
        "business_problem": "Large transformation programs often fail not from any single technical mistake, but from workstreams — process redesign, technical migration, change management — running in isolation from each other.",
        "approach": "We coordinate advisory, S/4HANA migration, integration, and change management as one program with a single roadmap, rather than treating them as separate vendor engagements.",
        "who_its_for": "Organizations planning a major SAP transformation spanning process change, S/4HANA migration, and organizational readiness.",
        "cta_label": "Discuss Your Transformation Program",
        "order": 1,
        "what_this_includes": [
            "SAP Consulting for roadmap and architecture",
            "S/4HANA migration execution",
            "Integration across the transformed landscape",
            "Testing and organizational change management",
        ],
        "outcomes_addressed": [
            "Modernize legacy SAP landscapes",
            "Scale enterprise architecture for future growth",
            "Optimize business processes end-to-end",
        ],
        "related_services": ["sap-consulting", "sap-s4hana", "sap-integration", "sap-testing"],
        "faqs": [
            (
                "How is this different from just buying S/4HANA migration services?",
                "Transformation coordinates migration alongside process redesign, integration, and change management as one program, rather than a purely technical conversion.",
            ),
            (
                "How long does a typical transformation program run?",
                "It varies significantly by landscape complexity and scope — usually discussed concretely after the initial assessment phase.",
            ),
        ],
    },
    {
        "slug": "sap-modernization",
        "name": "SAP Modernization",
        "short_summary": "Targeted modernization of specific processes or systems without a full-scale transformation.",
        "hero_intro": "Not every SAP challenge needs a full transformation program — sometimes the right move is modernizing a specific process, module, or integration point.",
        "business_problem": "Organizations sometimes delay fixing a specific outdated process or system because it feels tied to a much larger, riskier transformation decision.",
        "approach": "We scope modernization work narrowly around the specific process or system causing friction, so it can move forward independent of a broader transformation timeline.",
        "who_its_for": "Organizations with a specific outdated process, custom development, or system that needs modernizing without a full landscape overhaul.",
        "cta_label": "Discuss Modernization Options",
        "order": 2,
        "what_this_includes": [
            "Targeted process or module modernization",
            "Legacy custom code remediation",
            "Selective UI modernization with Fiori",
        ],
        "outcomes_addressed": [
            "Modernize legacy SAP landscapes",
            "Optimize business processes and system performance",
        ],
        "related_services": ["sap-consulting", "sap-development", "sap-implementation"],
        "faqs": [
            (
                "Can modernization work happen alongside a live system with no downtime window?",
                "Most targeted modernization work is scoped to minimize or avoid downtime — we assess this specifically during scoping.",
            ),
            (
                "Does this require a separate SAP license or module?",
                "Not usually — modernization typically works within your existing licensed footprint.",
            ),
        ],
    },
    {
        "slug": "cloud-transformation",
        "name": "Cloud Transformation",
        "short_summary": "Moving SAP workloads to the cloud without disrupting the business processes that depend on them.",
        "hero_intro": "Cloud transformation for SAP is about more than infrastructure — it's an opportunity to rethink how the landscape is architected and operated.",
        "business_problem": "Lift-and-shift cloud migrations often just relocate existing technical debt rather than resolving it, missing the chance to improve architecture along the way.",
        "approach": "We assess whether a workload should be lifted-and-shifted, re-platformed, or re-architected, then execute the cloud migration with that distinction in mind.",
        "who_its_for": "Organizations moving SAP infrastructure to the cloud, or evaluating RISE with SAP and similar cloud offerings.",
        "cta_label": "Discuss Your Cloud Move",
        "order": 3,
        "what_this_includes": [
            "Cloud readiness assessment",
            "Infrastructure migration execution",
            "Post-migration architecture optimization",
        ],
        "outcomes_addressed": ["Scale enterprise architecture", "Modernize legacy SAP landscapes"],
        "related_services": ["sap-consulting", "sap-migration", "sap-btp"],
        "faqs": [
            (
                "Do you support RISE with SAP migrations?",
                "Yes — we assess whether RISE or a self-managed cloud approach fits your operating model before recommending a path.",
            ),
            (
                "Will our customizations survive a cloud move?",
                "Custom code is assessed as part of the cloud readiness review, since it directly affects which migration approach makes sense.",
            ),
        ],
    },
    {
        "slug": "sap-integration",
        "name": "SAP Integration",
        "short_summary": "A connected enterprise ecosystem, not just a set of point-to-point interfaces.",
        "hero_intro": "Integration as a business outcome is bigger than any single interface — it's about SAP working as one connected part of your wider technology ecosystem.",
        "business_problem": "Individually well-built integrations can still add up to an ecosystem no one fully understands, because they were never designed against a shared architecture.",
        "approach": "We design integration at the ecosystem level first — architecture, governance, and monitoring — then build individual integrations against that shared foundation.",
        "who_its_for": "Organizations whose SAP landscape needs to work as one connected part of a broader enterprise ecosystem, not a set of isolated interfaces.",
        "cta_label": "Discuss Your Integration Strategy",
        "order": 4,
        "what_this_includes": [
            "Integration architecture and governance",
            "SAP Integration service delivery",
            "SAP BTP-based extension and automation",
        ],
        "outcomes_addressed": ["Integrate SAP with the wider enterprise ecosystem", "Scale enterprise architecture"],
        "related_services": ["sap-integration", "sap-btp", "sap-data-analytics"],
        "faqs": [
            (
                "How is this different from the SAP Integration service?",
                "The Integration service builds specific interfaces; this solution covers the architecture and governance that keeps all of them coherent as the landscape grows.",
            ),
            (
                "Do you work with our existing integration platform?",
                "Yes — we design around your existing middleware and tooling where it makes sense rather than defaulting to a replacement.",
            ),
        ],
    },
    {
        "slug": "automation",
        "name": "Automation",
        "short_summary": "Automating manual SAP processes using BTP, workflow, and AI where they create measurable value.",
        "hero_intro": "Manual work inside SAP processes is often invisible until you map it out — and much of it can be automated without custom development.",
        "business_problem": "Manual, repetitive steps inside SAP processes consume staff time that could go toward higher-value work, but are rarely prioritized because no single step looks large on its own.",
        "approach": "We map manual steps across a process end-to-end, then apply the right tool for each — standard workflow, BTP automation, or AI — rather than assuming one technology fits everything.",
        "who_its_for": "Organizations with manual, repetitive SAP processes that consume significant staff time.",
        "cta_label": "Discuss Automation Opportunities",
        "order": 5,
        "what_this_includes": [
            "Process mapping to identify automation candidates",
            "SAP BTP-based workflow automation",
            "AI-assisted automation where it creates clear value",
        ],
        "outcomes_addressed": ["Innovate using automation and AI", "Optimize business processes and system performance"],
        "related_services": ["sap-btp", "sap-data-analytics", "sap-development"],
        "faqs": [
            (
                "Do we need SAP BTP already provisioned to start?",
                "No — provisioning BTP is typically part of the automation engagement itself if it isn't already in place.",
            ),
            (
                "What kinds of processes automate well?",
                "High-volume, rules-based steps — approvals, data entry, reconciliation — tend to automate cleanly; judgment-heavy exceptions usually stay manual by design.",
            ),
        ],
    },
    {
        "slug": "data-ai",
        "name": "Data & AI",
        "short_summary": "A consistent data foundation, with AI applied where it creates measurable business value.",
        "hero_intro": "AI initiatives on top of SAP data tend to succeed or fail based on the data foundation underneath them, not the sophistication of the model.",
        "business_problem": "Organizations often pursue AI use cases before addressing the inconsistent, siloed data underneath them, leading to pilots that never make it to production.",
        "approach": "We build a consistent core data model first, then scope AI use cases against it, prioritizing ones with a clear path to measurable business value.",
        "who_its_for": "Organizations wanting to apply data and AI to their SAP landscape without starting from inconsistent or siloed data.",
        "cta_label": "Discuss Your Data & AI Strategy",
        "order": 6,
        "what_this_includes": [
            "Core data model and reporting foundation",
            "AI use case scoping and feasibility assessment",
            "SAP Datasphere and Analytics Cloud implementation",
        ],
        "outcomes_addressed": ["Innovate using data and AI", "Optimize business processes and system performance"],
        "related_services": ["sap-data-analytics", "sap-integration"],
        "faqs": [
            (
                "Do you build the AI models yourselves?",
                "For most use cases we apply SAP's built-in AI capabilities (SAP Analytics Cloud, Joule, embedded ML) rather than building custom models from scratch.",
            ),
            (
                "What's a realistic first AI use case?",
                "Something with a clear feasibility assessment and measurable outcome — usually forecasting, anomaly detection, or document processing rather than a broad, open-ended initiative.",
            ),
        ],
    },
]


class Command(BaseCommand):
    help = "Seeds the 6 solution pages (Section 11) with real, concise content."

    @transaction.atomic
    def handle(self, *args, **options):
        for data in SOLUTIONS_DATA:
            solution, created = Solution.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "name": data["name"],
                    "short_summary": data["short_summary"],
                    "hero_intro": data["hero_intro"],
                    "business_problem": data["business_problem"],
                    "approach": data["approach"],
                    "who_its_for": data["who_its_for"],
                    "cta_label": data["cta_label"],
                    "order": data["order"],
                },
            )

            solution.list_items.all().delete()
            for section, key in (
                (SolutionListItem.WHAT_THIS_INCLUDES, "what_this_includes"),
                (SolutionListItem.OUTCOMES, "outcomes_addressed"),
            ):
                for index, text in enumerate(data[key]):
                    SolutionListItem.objects.create(solution=solution, section=section, text=text, order=index)

            solution.faqs.all().delete()
            for index, (question, answer) in enumerate(data["faqs"]):
                FAQ.objects.create(content_object=solution, question=question, answer=answer, order=index)

            related = Service.objects.filter(slug__in=data["related_services"])
            solution.related_services.set(related)

            self.stdout.write(f"{'Created' if created else 'Updated'} solution: {solution.name}")

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(SOLUTIONS_DATA)} solutions."))
