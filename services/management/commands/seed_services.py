"""
Seeds the 14 SAP service pages listed in Section 10 of the build spec.

Content is written directly from the spec's own descriptions of each service
category (Sections 5, 9, 10) — concise, business-focused copy per Section 29,
not fabricated credentials (no invented clients, stats, or certifications;
Section 2). Re-running this command is safe: it upserts by slug.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import FAQ
from services.models import Service, ServiceListItem

SERVICES_DATA = [
    {
        "slug": "sap-consulting",
        "name": "SAP Consulting",
        "short_summary": "Landscape assessment, transformation roadmap, and architecture advisory grounded in your current environment.",
        "hero_intro": "Before any transformation, implementation, or migration decision, you need an honest picture of where your SAP landscape stands today and what a realistic path forward looks like.",
        "business_problem": "Most SAP decisions get made without a clear view of the current landscape's technical debt, process gaps, or true readiness for change — leading to roadmaps built on assumptions rather than evidence.",
        "delivery_approach": "We start with a structured assessment of your systems, processes, and architecture, then translate findings into a prioritized roadmap your teams can actually execute against.",
        "engagement_model": "Typically delivered as a fixed-scope advisory engagement, often the first step before a larger implementation or transformation program begins.",
        "who_its_for": "IT and business leaders who need clarity on their SAP landscape before committing budget to a larger initiative.",
        "cta_label": "Discuss Your SAP Roadmap",
        "featured": True,
        "order": 1,
        "what_we_solve": [
            "Unclear technical debt across the current SAP landscape",
            "No prioritized path from current state to target architecture",
            "Business and IT disagreement on where to invest next",
        ],
        "capabilities": [
            "Landscape and architecture assessment",
            "Transformation roadmap development",
            "Process assessment against SAP best practice",
            "SAP modernization strategy",
        ],
        "technology": ["SAP ECC and S/4HANA", "SAP BTP", "SAP Solution Manager / Focused Insights"],
        "deliverables": [
            "Current-state landscape assessment report",
            "Prioritized transformation roadmap",
            "Architecture recommendations",
        ],
        "faqs": [
            (
                "How long does an assessment take?",
                "A typical landscape assessment runs two to four weeks depending on the number of systems and modules in scope.",
            ),
            (
                "Do we need to commit to implementation work afterward?",
                "No — the assessment stands on its own. Many clients use it purely to inform an internal business case.",
            ),
        ],
    },
    {
        "slug": "sap-s4hana",
        "name": "SAP S/4HANA",
        "short_summary": "Greenfield, brownfield, and system conversion paths to S/4HANA, planned around business risk.",
        "hero_intro": "Moving to S/4HANA is as much a business decision as a technical one — the right path depends on your current ECC customizations, data quality, and appetite for process change.",
        "business_problem": "Organizations often default to the migration path a vendor or integrator prefers, rather than the one that fits their actual risk tolerance, timeline, and custom code footprint.",
        "delivery_approach": "We assess your current ECC landscape, custom code, and business processes to recommend greenfield, brownfield, or selective data transition — then execute against whichever path fits.",
        "engagement_model": "Runs as a project-based transformation program, typically phased across assessment, build, test, and cutover.",
        "who_its_for": "Organizations on SAP ECC evaluating or actively planning their move to S/4HANA.",
        "cta_label": "Discuss Your S/4HANA Roadmap",
        "featured": True,
        "order": 2,
        "what_we_solve": [
            "Uncertainty over greenfield vs. brownfield vs. selective data transition",
            "Custom code that won't survive a straight technical conversion",
            "Business processes that need rethinking, not just re-platforming",
        ],
        "capabilities": [
            "System conversion (brownfield)",
            "New implementation (greenfield)",
            "Selective data transition",
            "Post-go-live hypercare and optimization",
        ],
        "technology": ["S/4HANA Cloud and on-premise", "SAP Readiness Check", "SAP Custom Code Migration app"],
        "deliverables": [
            "Conversion vs. greenfield recommendation with rationale",
            "Migration and cutover plan",
            "Post-go-live stabilization support",
        ],
        "faqs": [
            (
                "Which path is right for us — greenfield or brownfield?",
                "It depends on your custom code volume, process debt, and timeline; our assessment gives you a specific recommendation rather than a default answer.",
            ),
            (
                "Can we migrate in phases by business unit or country?",
                "Yes — phased and selective data transition approaches are common for multi-entity organizations.",
            ),
        ],
    },
    {
        "slug": "sap-implementation",
        "name": "SAP Implementation",
        "short_summary": "Functional consulting, configuration, and testing through to a stable go-live.",
        "hero_intro": "A successful SAP implementation depends on disciplined delivery — clear scope, realistic testing, and a cutover plan that accounts for how your business actually operates.",
        "business_problem": "Implementations slip or destabilize the business when scope, testing, and organizational change management are treated as afterthoughts rather than core workstreams.",
        "delivery_approach": "We run implementation as a structured program — configuration and development in parallel with testing and training, so go-live isn't the first time users see the system.",
        "engagement_model": "Project-based delivery, usually with a dedicated team embedded alongside your internal stakeholders for the program's duration.",
        "who_its_for": "Organizations implementing SAP for the first time, or rolling it out to a new business unit or region.",
        "cta_label": "Plan Your Implementation",
        "featured": True,
        "order": 3,
        "what_we_solve": [
            "Scope creep with no clear configuration baseline",
            "Testing treated as a final-week activity instead of continuous",
            "Cutover risk from under-rehearsed data migration",
        ],
        "capabilities": [
            "Functional consulting and configuration",
            "Custom development where standard SAP doesn't fit",
            "Test planning and execution",
            "Cutover and go-live support",
        ],
        "technology": ["SAP S/4HANA", "SAP Activate methodology", "SAP Fiori"],
        "deliverables": [
            "Configuration documentation",
            "Test scripts and UAT sign-off",
            "Cutover runbook",
            "Go-live and hypercare support",
        ],
        "faqs": [
            (
                "What methodology do you use?",
                "SAP Activate, adapted to your organization's governance and change-management needs.",
            ),
            (
                "Do you handle end-user training?",
                "Yes, as part of the implementation program or as a standalone engagement — see SAP Training.",
            ),
        ],
    },
    {
        "slug": "sap-migration",
        "name": "SAP Migration",
        "short_summary": "Technical migration of SAP systems, data, and custom code with minimal business disruption.",
        "hero_intro": "System migrations — version upgrades, cloud moves, or data center transitions — carry real technical risk if the underlying data and dependencies aren't fully understood.",
        "business_problem": "Migrations that skip proper data profiling and dependency mapping tend to surface critical issues during cutover, when there's the least room to fix them.",
        "delivery_approach": "We profile source systems and data early, build a migration and fallback plan, and rehearse cutover before the production event.",
        "engagement_model": "Project-based, scoped around a specific migration event with a defined cutover window.",
        "who_its_for": "Organizations moving SAP systems between infrastructure, versions, or hosting environments.",
        "cta_label": "Discuss Your Migration Plan",
        "featured": False,
        "order": 4,
        "what_we_solve": [
            "Data quality issues discovered too late to fix before cutover",
            "Undocumented interface and custom code dependencies",
            "No tested rollback plan if cutover fails",
        ],
        "capabilities": [
            "Data profiling and cleansing",
            "Migration tooling and execution",
            "Interface and dependency mapping",
            "Cutover rehearsal and rollback planning",
        ],
        "technology": ["SAP Migration Cockpit", "SAP Data Services", "Database and OS migration tooling"],
        "deliverables": [
            "Data quality assessment",
            "Migration runbook with rollback plan",
            "Post-migration validation report",
        ],
        "faqs": [
            (
                "How do you minimize downtime during cutover?",
                "Through rehearsed mock migrations and a runbook that sequences tasks to shrink the actual production cutover window.",
            ),
            (
                "Can you migrate customizations along with standard data?",
                "Yes — custom objects and configuration are mapped and migrated alongside standard master and transactional data.",
            ),
        ],
    },
    {
        "slug": "sap-integration",
        "name": "SAP Integration",
        "short_summary": "SAP-to-SAP and SAP-to-non-SAP integration via APIs, middleware, and BTP Integration Suite.",
        "hero_intro": "SAP rarely operates in isolation — the value of your landscape depends on how reliably it exchanges data with everything else your business runs on.",
        "business_problem": "Point-to-point integrations built ad hoc over time become fragile, hard to monitor, and expensive to change whenever a connected system updates.",
        "delivery_approach": "We design integration architecture around reusable patterns and centralized monitoring, rather than one-off connections that only one person understands.",
        "engagement_model": "Ranges from project-based integration builds to ongoing integration platform management.",
        "who_its_for": "Organizations connecting SAP with CRM, e-commerce, logistics, banking, or other enterprise systems.",
        "cta_label": "Discuss Your Integration Challenge",
        "featured": True,
        "order": 5,
        "what_we_solve": [
            "Fragile point-to-point integrations with no central monitoring",
            "SAP-to-non-SAP data exchange that breaks on every system update",
            "No clear integration architecture as the landscape grows",
        ],
        "capabilities": [
            "SAP-to-SAP integration",
            "SAP-to-non-SAP integration via APIs and middleware",
            "BTP Integration Suite implementation",
            "Integration monitoring and error handling",
        ],
        "technology": ["SAP BTP Integration Suite", "SAP PI/PO", "REST and OData APIs", "Enterprise service bus platforms"],
        "deliverables": [
            "Integration architecture blueprint",
            "Built and tested integration flows",
            "Monitoring and alerting setup",
        ],
        "faqs": [
            (
                "Do you work with non-SAP middleware we already use?",
                "Yes — we integrate with your existing middleware where it makes sense, rather than defaulting to a full replatform.",
            ),
            (
                "How do you handle integration failures in production?",
                "Through structured monitoring and alerting so failures are caught and triaged before they affect downstream processes.",
            ),
        ],
    },
    {
        "slug": "sap-btp",
        "name": "SAP BTP",
        "short_summary": "Extensions, application development, and automation on SAP's cloud platform.",
        "hero_intro": "SAP BTP lets you extend and automate around your core SAP systems without touching stable core configuration — if the platform is set up with the right governance.",
        "business_problem": "Without clear extension governance, BTP projects can turn into as much technical debt as the custom ABAP they were meant to replace.",
        "delivery_approach": "We build extensions using SAP's clean-core principles — keeping customizations in BTP rather than the core system — so upgrades stay straightforward.",
        "engagement_model": "Typically project-based for individual extensions, with ongoing support available once extensions are in production.",
        "who_its_for": "Organizations wanting to extend SAP functionality without customizing the core system.",
        "cta_label": "Discuss Your SAP Extension Strategy",
        "featured": True,
        "order": 6,
        "what_we_solve": [
            "Custom requirements that would otherwise mean modifying SAP's core code",
            "No clean-core strategy as extension projects multiply",
            "Automation opportunities left unaddressed because they don't fit standard SAP",
        ],
        "capabilities": [
            "SAP BTP application development",
            "Integration Suite and Automation Suite implementation",
            "API and data services development",
            "Cloud-native extension architecture",
        ],
        "technology": ["SAP BTP (Cloud Foundry and Kyma)", "SAP Build", "CAP (Cloud Application Programming Model)"],
        "deliverables": [
            "Extension architecture and governance model",
            "Built and deployed BTP applications",
            "Documentation for internal maintenance",
        ],
        "faqs": [
            (
                "What is 'clean core' and why does it matter?",
                "It means keeping custom logic out of SAP's core system and in BTP instead, so upgrades don't break your customizations.",
            ),
            (
                "Can you build on BTP alongside our internal developers?",
                "Yes — we often work as an extension of an internal team, transferring knowledge as we go.",
            ),
        ],
    },
    {
        "slug": "sap-development",
        "name": "SAP Development",
        "short_summary": "ABAP, ABAP Cloud, Fiori, and UI5 development for custom applications built to be maintained.",
        "hero_intro": "Custom SAP development is sometimes unavoidable — the question is whether it's built in a way your team can maintain, or a way that becomes a liability at the next upgrade.",
        "business_problem": "Legacy custom ABAP written without documentation or upgrade discipline tends to become the single biggest blocker to future SAP upgrades.",
        "delivery_approach": "We write custom developments against SAP's current standards — ABAP Cloud and RAP where possible — with documentation that survives staff turnover.",
        "engagement_model": "Project-based for discrete developments, or staff augmentation for teams needing ongoing development capacity.",
        "who_its_for": "Organizations with requirements standard SAP configuration can't meet.",
        "cta_label": "Discuss Your SAP Development Needs",
        "featured": True,
        "order": 7,
        "what_we_solve": [
            "Custom requirements standard configuration can't satisfy",
            "Legacy ABAP with no documentation and no clear owner",
            "Custom UIs that don't match how users actually work",
        ],
        "capabilities": [
            "ABAP and ABAP Cloud development",
            "Fiori and UI5 application development",
            "OData service development",
            "Custom reports, forms, and workflows",
        ],
        "technology": ["ABAP Cloud / RAP", "SAP Fiori Elements", "SAP Gateway / OData"],
        "deliverables": [
            "Custom application or report, tested and documented",
            "Technical specification and code documentation",
            "Handover and knowledge transfer session",
        ],
        "faqs": [
            (
                "Do you develop in classic ABAP or only ABAP Cloud?",
                "We default to ABAP Cloud and RAP for new development where the target system supports it, and classic ABAP where it doesn't.",
            ),
            (
                "Will your code be maintainable by our internal team?",
                "Yes — every development ships with documentation and a handover session with your team.",
            ),
        ],
    },
    {
        "slug": "sap-ams",
        "name": "SAP AMS & Support",
        "short_summary": "Application support, incident management, and continuous enhancement for live SAP systems.",
        "hero_intro": "Once SAP is live, the work doesn't stop — it shifts from delivery to keeping the system reliable while it keeps evolving with the business.",
        "business_problem": "Support backlogs grow when incidents, enhancements, and minor projects all compete for the same small internal team's time, with no structured triage.",
        "delivery_approach": "We run AMS on a structured incident and enhancement backlog, with clear SLAs for response and resolution based on severity.",
        "engagement_model": "Ongoing managed service, typically billed on a retainer or ticket-volume basis.",
        "who_its_for": "Organizations with live SAP systems needing structured, ongoing application support.",
        "cta_label": "Explore SAP Support Options",
        "featured": True,
        "order": 8,
        "what_we_solve": [
            "Growing support backlog with no clear prioritization",
            "Incidents and enhancements competing for the same limited resources",
            "No structured handover from project team to support team post-go-live",
        ],
        "capabilities": [
            "Incident and problem management",
            "Enhancement backlog management",
            "Performance monitoring",
            "Release management for SAP changes",
        ],
        "technology": ["SAP Solution Manager", "ITSM/ticketing platforms (ServiceNow, Jira Service Management)", "SAP EarlyWatch Alert"],
        "deliverables": [
            "Defined SLA and severity framework",
            "Monthly service reporting",
            "Continuous improvement backlog",
        ],
        "faqs": [
            (
                "What response times can we expect?",
                "Response and resolution targets are agreed per severity level as part of the engagement scope, not a fixed default across all clients.",
            ),
            (
                "Can you take over support from our current provider?",
                "Yes — we run a structured knowledge-transfer period before taking full ownership of the support backlog.",
            ),
        ],
    },
    {
        "slug": "sap-managed-services",
        "name": "SAP Managed Services",
        "short_summary": "Ongoing operational ownership of your SAP landscape — monitoring, releases, and continuous improvement.",
        "hero_intro": "Managed services go beyond ticket-based support to full operational ownership of your SAP landscape's day-to-day health and evolution.",
        "business_problem": "Internal teams often end up owning SAP operations as a side responsibility, without the dedicated capacity to do proactive monitoring or planned improvement.",
        "delivery_approach": "We take structured ownership of monitoring, release management, and a continuous improvement roadmap, reporting against agreed operational metrics.",
        "engagement_model": "Ongoing managed service, typically the natural next step after AMS once an organization wants fuller operational ownership handed over.",
        "who_its_for": "Organizations wanting to hand over day-to-day SAP operations rather than manage them internally.",
        "cta_label": "Explore Managed Services",
        "featured": False,
        "order": 9,
        "what_we_solve": [
            "No dedicated capacity for proactive SAP operations",
            "Release and change management handled reactively",
            "No continuous improvement roadmap for the live system",
        ],
        "capabilities": [
            "Proactive system monitoring",
            "Release and change management",
            "Continuous improvement planning",
            "Vendor and landscape ownership",
        ],
        "technology": ["SAP Solution Manager / Focused Run", "SAP Cloud ALM", "Monitoring and alerting platforms"],
        "deliverables": [
            "Operational runbook",
            "Regular health and performance reporting",
            "Continuous improvement roadmap",
        ],
        "faqs": [
            (
                "How is this different from AMS?",
                "AMS is primarily ticket-based support; managed services is broader operational ownership, including proactive monitoring and a continuous improvement roadmap.",
            ),
            (
                "Do you take over infrastructure as well as application support?",
                "That depends on scope — some engagements include infrastructure and Basis, others focus purely on the application layer.",
            ),
        ],
    },
    {
        "slug": "sap-support",
        "name": "SAP Support",
        "short_summary": "Responsive, incident-focused support for day-to-day SAP issues.",
        "hero_intro": "Sometimes what you need isn't a full managed-service relationship — just reliable, responsive support when something breaks.",
        "business_problem": "Small and mid-sized SAP teams often can't justify a full internal support function, but still need fast, reliable help when incidents happen.",
        "delivery_approach": "We provide a responsive service desk for SAP incidents, triaged by severity, with escalation paths for issues that need deeper specialist involvement.",
        "engagement_model": "Available as a standalone reactive support engagement, or as the first tier within a broader AMS relationship.",
        "who_its_for": "Organizations needing responsive break-fix support without committing to a full AMS or managed-services scope.",
        "cta_label": "Talk to SAP Support",
        "featured": False,
        "order": 10,
        "what_we_solve": [
            "No reliable point of contact when SAP issues arise",
            "Internal team stretched thin by day-to-day break-fix work",
            "Slow escalation paths for issues beyond first-line capability",
        ],
        "capabilities": [
            "Incident triage and service desk",
            "Break-fix resolution",
            "Escalation to specialist consultants where needed",
            "Basic system health checks",
        ],
        "technology": ["ITSM/ticketing platforms", "SAP Solution Manager"],
        "deliverables": [
            "Defined support scope and escalation path",
            "Incident resolution log",
            "Recurring issue trend reporting",
        ],
        "faqs": [
            (
                "Is this the same as AMS?",
                "Support is the reactive, incident-focused layer; AMS adds structured enhancement and backlog management on top of it.",
            ),
            (
                "Can we scale up to AMS later?",
                "Yes — support engagements commonly expand into full AMS as needs grow.",
            ),
        ],
    },
    {
        "slug": "sap-security",
        "name": "SAP Security",
        "short_summary": "Authorization design, segregation of duties, and security architecture review for SAP landscapes.",
        "hero_intro": "SAP security is often treated as an afterthought until an audit finding or incident forces attention — by then, remediation is far more disruptive.",
        "business_problem": "Authorization models that grow organically over years tend to accumulate excessive access and segregation-of-duties conflicts that go unnoticed until an audit.",
        "delivery_approach": "We review your current authorization landscape against segregation-of-duties principles and rebuild roles where needed, with minimal disruption to daily operations.",
        "engagement_model": "Typically a project-based assessment and remediation engagement, with ongoing security monitoring available afterward.",
        "who_its_for": "Organizations facing audit findings, preparing for one, or rebuilding SAP authorizations as part of a broader transformation.",
        "cta_label": "Assess Your SAP Security",
        "featured": False,
        "order": 11,
        "what_we_solve": [
            "Segregation-of-duties conflicts accumulated over years",
            "Excessive or unclear user access",
            "No structured process for reviewing authorization changes",
        ],
        "capabilities": [
            "Authorization concept design",
            "Segregation-of-duties analysis",
            "Security architecture review",
            "GRC tool implementation support",
        ],
        "technology": ["SAP GRC Access Control", "SAP Identity Management", "SoD analysis tooling"],
        "deliverables": [
            "Segregation-of-duties risk report",
            "Redesigned authorization concept",
            "Remediation plan",
        ],
        "faqs": [
            (
                "Will fixing SoD conflicts disrupt daily operations?",
                "Remediation is phased and tested against real user activity first, specifically to avoid blocking legitimate day-to-day work.",
            ),
            (
                "Do you support GRC tool implementations?",
                "Yes, including SAP GRC Access Control configuration alongside the underlying authorization redesign.",
            ),
        ],
    },
    {
        "slug": "sap-data-analytics",
        "name": "SAP Data, Analytics & AI",
        "short_summary": "Reporting, planning, and data modeling, plus AI use cases where they create measurable value.",
        "hero_intro": "SAP systems generate enormous amounts of data — the challenge is usually turning it into decisions, not collecting more of it.",
        "business_problem": "Reporting built around individual requests, rather than a coherent data model, tends to produce inconsistent numbers across departments.",
        "delivery_approach": "We build reporting and planning on a consistent underlying data model first, then layer analytics and automation on top of it.",
        "engagement_model": "Project-based for initial data model and reporting builds, with ongoing support for expanding scope over time.",
        "who_its_for": "Organizations whose SAP reporting has become inconsistent or hard to trust across departments.",
        "cta_label": "Discuss Your Data Strategy",
        "featured": True,
        "order": 12,
        "what_we_solve": [
            "Inconsistent numbers across departmental reports",
            "Manual reporting processes that don't scale",
            "AI and automation ideas with no clear starting point",
        ],
        "capabilities": [
            "Analytics and reporting design",
            "SAP Datasphere implementation",
            "Planning and data modeling",
            "AI use case identification and scoping",
        ],
        "technology": ["SAP Datasphere", "SAP Analytics Cloud", "SAP BW/4HANA"],
        "deliverables": [
            "Consistent core data model",
            "Built reporting and planning solution",
            "AI use case shortlist with feasibility assessment",
        ],
        "faqs": [
            (
                "Where do most AI use cases actually create value in SAP?",
                "Areas with high-volume, repetitive decisions — demand forecasting, anomaly detection, and document processing — tend to show the clearest early returns.",
            ),
            (
                "Do we need to be on S/4HANA to modernize reporting?",
                "No — Datasphere and Analytics Cloud can connect to ECC as well as S/4HANA, though S/4HANA does simplify the underlying data model.",
            ),
        ],
    },
    {
        "slug": "sap-testing",
        "name": "SAP Testing",
        "short_summary": "Test strategy, regression testing, and UAT support for SAP implementations and transformations.",
        "hero_intro": "Testing is where SAP projects either catch problems early or discover them in production — the difference comes down to how rigorously it's planned.",
        "business_problem": "Testing squeezed into the final weeks of a project rarely covers enough scenarios to catch the issues that actually cause go-live disruption.",
        "delivery_approach": "We build a test strategy early in the project, covering functional, regression, and integration testing, with automation applied where it reduces long-term retesting effort.",
        "engagement_model": "Typically embedded within a larger implementation or transformation program, though standalone testing engagements are available for specific releases.",
        "who_its_for": "Organizations running SAP implementations, upgrades, or transformations that need structured test coverage.",
        "cta_label": "Discuss Your Testing Needs",
        "featured": False,
        "order": 13,
        "what_we_solve": [
            "Testing compressed into the final weeks before go-live",
            "No regression coverage for changes made during the project",
            "UAT that surfaces issues too late to fix cheaply",
        ],
        "capabilities": [
            "Test strategy and planning",
            "Automated regression testing",
            "UAT coordination and defect management",
            "Performance and load testing",
        ],
        "technology": ["SAP Test Automation Tool", "Tricentis Tosca", "SAP Solution Manager Test Suite"],
        "deliverables": [
            "Test strategy and coverage plan",
            "Automated regression test suite",
            "UAT sign-off and defect log",
        ],
        "faqs": [
            (
                "Can you automate regression testing for our custom transactions?",
                "Yes — automation is scoped to cover the transactions and processes most affected by ongoing change, not just standard SAP flows.",
            ),
            (
                "When should test planning start relative to the project timeline?",
                "As early as the design phase — building the test strategy alongside configuration avoids the compression that causes most go-live issues.",
            ),
        ],
    },
    {
        "slug": "sap-training",
        "name": "SAP Training",
        "short_summary": "End-user and super-user training designed around adoption, not just system familiarity.",
        "hero_intro": "A technically successful go-live can still fail on adoption if users don't understand the new processes behind the new screens.",
        "business_problem": "Generic, feature-by-feature training tends to produce users who can click through screens but don't understand the business process changes behind them.",
        "delivery_approach": "We build role-based training around actual business processes, with super-users identified and trained early enough to support their teams post-go-live.",
        "engagement_model": "Typically delivered within an implementation program's later phases, or as a standalone engagement ahead of a process change.",
        "who_its_for": "Organizations preparing users for a new SAP system, module, or significant process change.",
        "cta_label": "Plan Your Training Program",
        "featured": False,
        "order": 14,
        "what_we_solve": [
            "Users who complete training but don't understand the new process flow",
            "No super-user network to support colleagues after go-live",
            "Training materials that go stale as soon as the system changes",
        ],
        "capabilities": [
            "Role-based training content development",
            "Super-user enablement programs",
            "Go-live floor support",
            "Post-go-live adoption tracking",
        ],
        "technology": ["SAP Enable Now", "SAP Workforce Performance Builder"],
        "deliverables": [
            "Role-based training curriculum",
            "Trained super-user network",
            "Post-go-live adoption report",
        ],
        "faqs": [
            (
                "Do you build training content or just deliver it?",
                "Both — we typically build role-based content tailored to your configured processes, then deliver or train your internal trainers to deliver it.",
            ),
            (
                "How do you measure whether training actually worked?",
                "Through post-go-live adoption tracking — support ticket volume and process compliance are usually clearer signals than training completion rates alone.",
            ),
        ],
    },
]

# Cross-links between naturally related services (Section 10: "Related services").
RELATED_MAP = {
    "sap-consulting": ["sap-s4hana", "sap-security"],
    "sap-s4hana": ["sap-migration", "sap-implementation", "sap-testing"],
    "sap-implementation": ["sap-s4hana", "sap-testing", "sap-training"],
    "sap-migration": ["sap-s4hana", "sap-integration"],
    "sap-integration": ["sap-btp", "sap-data-analytics"],
    "sap-btp": ["sap-development", "sap-integration"],
    "sap-development": ["sap-btp", "sap-ams"],
    "sap-ams": ["sap-managed-services", "sap-support"],
    "sap-managed-services": ["sap-ams", "sap-support"],
    "sap-support": ["sap-ams", "sap-managed-services"],
    "sap-security": ["sap-ams", "sap-consulting"],
    "sap-data-analytics": ["sap-integration", "sap-btp"],
    "sap-testing": ["sap-implementation", "sap-s4hana"],
    "sap-training": ["sap-implementation"],
}


class Command(BaseCommand):
    help = "Seeds the 14 SAP service pages (Section 10) with real, concise content."

    @transaction.atomic
    def handle(self, *args, **options):
        for data in SERVICES_DATA:
            service, created = Service.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "name": data["name"],
                    "short_summary": data["short_summary"],
                    "hero_intro": data["hero_intro"],
                    "business_problem": data["business_problem"],
                    "delivery_approach": data["delivery_approach"],
                    "engagement_model": data["engagement_model"],
                    "who_its_for": data["who_its_for"],
                    "cta_label": data["cta_label"],
                    "featured": data["featured"],
                    "order": data["order"],
                },
            )

            service.list_items.all().delete()
            for section in (
                ServiceListItem.WHAT_WE_SOLVE,
                ServiceListItem.CAPABILITIES,
                ServiceListItem.TECHNOLOGY,
                ServiceListItem.DELIVERABLES,
            ):
                for index, text in enumerate(data[section]):
                    ServiceListItem.objects.create(service=service, section=section, text=text, order=index)

            service.faqs.all().delete()
            for index, (question, answer) in enumerate(data["faqs"]):
                FAQ.objects.create(content_object=service, question=question, answer=answer, order=index)

            self.stdout.write(f"{'Created' if created else 'Updated'} service: {service.name}")

        for slug, related_slugs in RELATED_MAP.items():
            try:
                service = Service.objects.get(slug=slug)
            except Service.DoesNotExist:
                continue
            service.related_services.set(Service.objects.filter(slug__in=related_slugs))

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(SERVICES_DATA)} services."))
