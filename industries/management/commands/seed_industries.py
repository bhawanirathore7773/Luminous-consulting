"""
Seeds the 12 industry pages listed in Section 12 of the build spec.

Section 12 explicitly warns against "simply replacing the industry name in
generic copy" — every field below is grounded in how SAP actually gets used
in that industry (module choices, integration needs, typical pain points),
not a shared template with the noun swapped out.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import FAQ
from industries.models import Industry, IndustryListItem
from services.models import Service

INDUSTRIES_DATA = [
    {
        "slug": "manufacturing",
        "name": "Manufacturing",
        "short_summary": "Production planning, quality management, and plant maintenance on a connected SAP core.",
        "hero_intro": "Manufacturing runs on the handoff between planning and the shop floor — SAP's value depends on how well that handoff actually works in practice.",
        "sap_landscape": "Most manufacturers run SAP ECC or S/4HANA for production planning and materials management, often alongside separate MES or shop-floor systems that were never fully integrated back into the core.",
        "outcomes": "Modernize and Integrate apply most directly here — connecting shop-floor data back into SAP is usually the highest-leverage move, followed by Optimize as production and quality processes tighten up.",
        "cta_label": "Discuss Your Manufacturing Challenge",
        "order": 1,
        "challenges": [
            "Production planning disconnected from real shop-floor data",
            "Quality issues caught too late in the process",
            "Siloed plant-level systems feeding inconsistent corporate reporting",
        ],
        "processes": ["Production planning and scheduling", "Quality management and inspection", "Plant maintenance"],
        "modules": ["PP", "QM", "PM", "MM"],
        "integration_requirements": ["MES / shop-floor systems", "IoT and sensor data", "Supplier EDI"],
        "transformation_opportunities": [
            "Predictive maintenance via IoT and BTP",
            "Digital twin for production lines",
            "Automated quality inspection",
        ],
        "typical_use_cases": [
            "Real-time production dashboards",
            "Machine downtime tracking",
            "Automated quality holds",
        ],
        "related_services": ["sap-implementation", "sap-integration", "sap-data-analytics"],
        "faqs": [
            (
                "Do you integrate with MES platforms we already run?",
                "Yes — integration is typically scoped around your existing MES rather than requiring a replacement.",
            ),
            (
                "Can predictive maintenance work with our existing sensors?",
                "In most cases — the assessment includes reviewing what sensor and historian data is already available before proposing an approach.",
            ),
        ],
    },
    {
        "slug": "automotive",
        "name": "Automotive",
        "short_summary": "Demand-driven planning and supplier collaboration for complex, variant-heavy production.",
        "hero_intro": "Automotive supply chains run on precise timing and heavy product variation — SAP needs to keep pace with both at once.",
        "sap_landscape": "Automotive manufacturers typically run SAP with variant configuration for complex product options, alongside dense supplier EDI networks and, increasingly, connected vehicle data feeds.",
        "outcomes": "Integrate is central here, given the density of supplier connections; Optimize follows closely as sequencing and JIT delivery processes are tightened.",
        "cta_label": "Discuss Your Automotive Challenge",
        "order": 2,
        "challenges": [
            "Complex multi-tier supplier coordination",
            "Just-in-time and sequence delivery pressure",
            "Variant-heavy product configuration",
        ],
        "processes": ["Demand-driven production planning", "Supplier collaboration and EDI", "Variant configuration"],
        "modules": ["PP-VC (variant configuration)", "MM", "SD", "EWM"],
        "integration_requirements": ["Supplier EDI (ANSI X12 and similar)", "Dealer/DMS systems", "Telematics data"],
        "transformation_opportunities": [
            "Demand sensing with AI",
            "Digital supplier collaboration portals",
            "Connected vehicle data integration",
        ],
        "typical_use_cases": [
            "Sequenced JIT delivery scheduling",
            "Warranty claim automation",
            "Supplier scorecarding",
        ],
        "related_services": ["sap-integration", "sap-implementation", "sap-btp"],
        "faqs": [
            (
                "Do you support EDI with our existing supplier network?",
                "Yes — EDI integration is scoped against your current supplier connections and standards.",
            ),
            (
                "Can variant configuration handle our current product complexity?",
                "SAP's variant configuration is built for exactly this kind of complexity; we assess your current model as part of scoping.",
            ),
        ],
    },
    {
        "slug": "pharma-life-sciences",
        "name": "Pharma & Life Sciences",
        "short_summary": "Batch genealogy, serialization, and validated compliance across the SAP landscape.",
        "hero_intro": "In pharma, SAP isn't just an operational system — it's part of how you prove compliance, batch by batch.",
        "sap_landscape": "Pharma and life sciences organizations typically run SAP with batch management and quality modules tightly coupled to serialization and track-and-trace networks required for regulatory compliance.",
        "outcomes": "Operate is central here, given the compliance burden of keeping a validated system reliable; Innovate applies cautiously, where AI can assist quality review without touching validated logic.",
        "cta_label": "Discuss Your Life Sciences Challenge",
        "order": 3,
        "challenges": [
            "Strict batch genealogy and traceability requirements",
            "Serialization and anti-counterfeiting compliance",
            "Validated system change control",
        ],
        "processes": ["Batch production and genealogy tracking", "Quality assurance and regulatory compliance", "Serialization"],
        "modules": ["QM", "PP (batch management)", "EHS"],
        "integration_requirements": ["Serialization / track-and-trace networks", "LIMS (lab systems)", "Regulatory reporting platforms"],
        "transformation_opportunities": [
            "Automated compliance reporting",
            "AI-assisted quality deviation analysis",
            "Digital batch records",
        ],
        "typical_use_cases": [
            "End-to-end batch traceability",
            "Expiry and quarantine management",
            "Regulatory submission support",
        ],
        "related_services": ["sap-security", "sap-implementation", "sap-testing"],
        "faqs": [
            (
                "How do you handle changes in a validated (GxP) system?",
                "Through documented, tested change control aligned to your existing validation procedures — we work within your QA process, not around it.",
            ),
            (
                "Do you have experience with serialization mandates?",
                "Yes — serialization integration is scoped against the specific regulatory markets you serialize for.",
            ),
        ],
    },
    {
        "slug": "retail-consumer",
        "name": "Retail & Consumer",
        "short_summary": "Omnichannel inventory, demand forecasting, and POS integration on a unified SAP core.",
        "hero_intro": "Retail customers expect a consistent experience across channels — that consistency has to be backed by a single, reliable view of inventory in SAP.",
        "sap_landscape": "Retailers typically run SAP for merchandising and inventory alongside separate POS and e-commerce platforms, often with inconsistent stock visibility between them.",
        "outcomes": "Integrate matters most here, unifying inventory across channels; Optimize follows as forecasting and replenishment improve.",
        "cta_label": "Discuss Your Retail Challenge",
        "order": 4,
        "challenges": [
            "Omnichannel inventory visibility",
            "Seasonal demand volatility",
            "Fragmented POS-to-ERP data flow",
        ],
        "processes": ["Demand forecasting and merchandising", "Omnichannel order fulfillment", "POS integration"],
        "modules": ["SD", "MM", "Retail/Fashion Management"],
        "integration_requirements": ["POS systems", "E-commerce platforms", "Third-party logistics"],
        "transformation_opportunities": [
            "AI-driven demand forecasting",
            "Unified commerce inventory",
            "Automated replenishment",
        ],
        "typical_use_cases": [
            "Click-and-collect fulfillment",
            "Dynamic pricing support",
            "Returns processing automation",
        ],
        "related_services": ["sap-integration", "sap-data-analytics", "sap-implementation"],
        "faqs": [
            (
                "Can you integrate with our existing POS and e-commerce platforms?",
                "Yes — integration is scoped around your current platforms rather than requiring a switch.",
            ),
            (
                "Does unifying inventory require a full replatform?",
                "Not necessarily — often it's an integration and data-model problem rather than a need to replace existing systems.",
            ),
        ],
    },
    {
        "slug": "logistics-supply-chain",
        "name": "Logistics & Supply Chain",
        "short_summary": "Warehouse management, transportation planning, and freight settlement connected to core ERP.",
        "hero_intro": "Warehouse and transportation execution generate huge amounts of operational data — the value comes from getting it back into SAP in near real time.",
        "sap_landscape": "Logistics organizations typically run SAP EWM and TM alongside carrier and telematics integrations that vary widely in how tightly they're connected back to the core.",
        "outcomes": "Integrate and Optimize apply most directly — real-time visibility and tighter process execution tend to deliver the clearest near-term value.",
        "cta_label": "Discuss Your Logistics Challenge",
        "order": 5,
        "challenges": [
            "Warehouse and transportation systems operating separately from core ERP",
            "Limited real-time shipment visibility",
            "Manual freight cost reconciliation",
        ],
        "processes": ["Warehouse management", "Transportation planning and execution", "Freight settlement"],
        "modules": ["EWM", "TM", "MM"],
        "integration_requirements": ["Carrier / EDI networks", "Telematics and GPS tracking", "Customs systems"],
        "transformation_opportunities": [
            "Automated freight audit",
            "Real-time shipment visibility dashboards",
            "Warehouse robotics integration",
        ],
        "typical_use_cases": [
            "Cross-dock optimization",
            "Automated carrier selection",
            "Freight cost reconciliation",
        ],
        "related_services": ["sap-integration", "sap-btp", "sap-data-analytics"],
        "faqs": [
            (
                "Do you work with our existing carrier and telematics providers?",
                "Yes — integration is built against your current carrier and tracking providers rather than a fixed list.",
            ),
            (
                "Can EWM and TM run alongside our current WMS?",
                "It depends on your target architecture; we assess whether to integrate, replace, or run in parallel during scoping.",
            ),
        ],
    },
    {
        "slug": "energy-utilities",
        "name": "Energy & Utilities",
        "short_summary": "Metering, billing, and asset maintenance at regulatory-grade scale and accuracy.",
        "hero_intro": "Utilities operate at a scale and regulatory scrutiny where metering, billing, and asset maintenance all have to work reliably at once.",
        "sap_landscape": "Utilities typically run SAP IS-U for metering and billing alongside plant maintenance modules, with growing volumes of smart-meter and SCADA data to absorb.",
        "outcomes": "Operate is central given the asset-heavy, regulated nature of the business; Innovate applies through smart-meter analytics once the operational core is solid.",
        "cta_label": "Discuss Your Utilities Challenge",
        "order": 6,
        "challenges": [
            "Complex metering and billing at scale",
            "Regulatory reporting obligations",
            "Asset-heavy maintenance planning",
        ],
        "processes": ["Metering and billing", "Asset and plant maintenance", "Regulatory compliance reporting"],
        "modules": ["IS-U (Utilities)", "PM", "EHS"],
        "integration_requirements": ["Smart meter / AMI data", "SCADA systems", "Regulatory reporting platforms"],
        "transformation_opportunities": [
            "Predictive asset maintenance",
            "Smart-meter analytics",
            "Automated regulatory reporting",
        ],
        "typical_use_cases": [
            "Usage-based billing automation",
            "Outage management integration",
            "Asset lifecycle tracking",
        ],
        "related_services": ["sap-implementation", "sap-ams", "sap-data-analytics"],
        "faqs": [
            (
                "Can SAP IS-U handle our current billing volume?",
                "IS-U is built for utility-scale metering and billing; specific volume and performance requirements are reviewed during assessment.",
            ),
            (
                "Do you integrate with SCADA systems?",
                "Yes — SCADA and smart-meter integration is scoped against your existing infrastructure.",
            ),
        ],
    },
    {
        "slug": "engineering-construction",
        "name": "Engineering & Construction",
        "short_summary": "Project cost control, procurement, and progress billing across long-cycle projects.",
        "hero_intro": "Engineering and construction projects run for months or years — SAP needs to give accurate cost and progress visibility throughout, not just at close.",
        "sap_landscape": "E&C organizations typically run SAP Project Systems alongside procurement and subcontractor management, often with budget-to-actual reporting that lags real project status.",
        "outcomes": "Optimize applies most directly through tighter cost control; Scale matters as multi-project resource allocation becomes the bottleneck.",
        "cta_label": "Discuss Your Engineering & Construction Challenge",
        "order": 7,
        "challenges": [
            "Long-cycle project cost tracking",
            "Subcontractor and procurement coordination",
            "Budget-to-actual visibility across projects",
        ],
        "processes": ["Project systems and cost control", "Procurement and subcontractor management", "Project billing"],
        "modules": ["PS (Project Systems)", "MM", "SD"],
        "integration_requirements": ["Project scheduling tools", "Subcontractor portals", "Field data capture"],
        "transformation_opportunities": [
            "Real-time project cost dashboards",
            "Automated progress billing",
            "Resource capacity planning",
        ],
        "typical_use_cases": [
            "Milestone-based billing",
            "Change-order tracking",
            "Multi-project resource allocation",
        ],
        "related_services": ["sap-implementation", "sap-data-analytics"],
        "faqs": [
            (
                "Does SAP PS integrate with our project scheduling tools?",
                "Yes — integration with common scheduling tools is scoped as part of the project systems implementation.",
            ),
            (
                "Can billing follow our specific milestone structure?",
                "Milestone billing configuration is built around your actual contract and billing terms, not a generic default.",
            ),
        ],
    },
    {
        "slug": "professional-services",
        "name": "Professional Services",
        "short_summary": "Project profitability, resource utilization, and revenue recognition for services firms.",
        "hero_intro": "For a services firm, the SAP question that matters most is simple: is this engagement actually profitable, and can you see that in real time?",
        "sap_landscape": "Professional services firms typically run SAP Project Systems and controlling modules alongside separate time-tracking and CRM tools that don't always feed profitability reporting cleanly.",
        "outcomes": "Optimize is central through better utilization and margin visibility; Integrate matters where time-tracking and CRM data needs to flow back into project accounting.",
        "cta_label": "Discuss Your Professional Services Challenge",
        "order": 8,
        "challenges": [
            "Project profitability visibility",
            "Resource utilization tracking",
            "Time and billing accuracy across engagements",
        ],
        "processes": ["Project-based resource planning", "Time and expense management", "Project billing and revenue recognition"],
        "modules": ["PS", "SD", "CO (controlling)"],
        "integration_requirements": ["Time-tracking tools", "CRM systems", "Expense management platforms"],
        "transformation_opportunities": [
            "Automated utilization reporting",
            "Real-time project margin tracking",
            "Revenue recognition automation",
        ],
        "typical_use_cases": [
            "Engagement profitability dashboards",
            "Resource staffing optimization",
            "Automated invoicing",
        ],
        "related_services": ["sap-implementation", "sap-data-analytics"],
        "faqs": [
            (
                "Can this integrate with the time-tracking tool we already use?",
                "Yes — integration is scoped around your current time-tracking and CRM tools rather than requiring a switch.",
            ),
            (
                "How quickly can we see engagement-level margin data?",
                "That depends on your current data model; consistent, near-real-time margin reporting is typically the core deliverable of this kind of engagement.",
            ),
        ],
    },
    {
        "slug": "healthcare",
        "name": "Healthcare",
        "short_summary": "Clinical supply chain, facility maintenance, and compliance-driven operations.",
        "hero_intro": "Healthcare operations run on tight compliance requirements and the need for critical supplies and equipment to always be available.",
        "sap_landscape": "Healthcare organizations typically run SAP for clinical supply chain and facility maintenance, integrated carefully with hospital information systems given the sensitivity of the data involved.",
        "outcomes": "Operate is central given the compliance and availability requirements; Optimize follows through tighter supply chain and maintenance processes.",
        "cta_label": "Discuss Your Healthcare Challenge",
        "order": 9,
        "challenges": [
            "Patient-related data handled under strict privacy and compliance requirements",
            "Complex procurement for clinical supplies",
            "Asset-heavy facility and equipment management",
        ],
        "processes": ["Clinical supply chain and procurement", "Facility and equipment maintenance", "Regulatory compliance"],
        "modules": ["MM", "PM", "EHS"],
        "integration_requirements": ["Hospital information systems", "Medical device data", "Regulatory reporting platforms"],
        "transformation_opportunities": [
            "Predictive equipment maintenance",
            "Automated compliance documentation",
            "Supply chain visibility for critical items",
        ],
        "typical_use_cases": [
            "Clinical asset tracking",
            "Procurement automation for medical supplies",
            "Compliance audit reporting",
        ],
        "related_services": ["sap-security", "sap-ams", "sap-implementation"],
        "faqs": [
            (
                "How do you handle integration involving sensitive patient data?",
                "Integration scope is defined to keep clinical/patient data within your existing compliant systems, exchanging only what SAP genuinely needs for supply chain and asset processes.",
            ),
            (
                "Can you support high-availability requirements for critical supplies?",
                "Yes — availability and criticality requirements are part of scoping the supply chain and procurement design.",
            ),
        ],
    },
    {
        "slug": "banking-financial-services",
        "name": "Banking & Financial Services",
        "short_summary": "Financial consolidation, regulatory reporting, and treasury on a controlled SAP core.",
        "hero_intro": "In financial services, SAP's accuracy and auditability matter as much as its functionality — regulators expect both.",
        "sap_landscape": "Banking and financial services organizations typically run SAP FI/CO for financial accounting and consolidation, integrated with core banking and risk systems under strict audit requirements.",
        "outcomes": "Operate and Optimize are central here, given the premium on accuracy and controlled processes over rapid change.",
        "cta_label": "Discuss Your Financial Services Challenge",
        "order": 10,
        "challenges": [
            "Strict regulatory and audit requirements",
            "High-volume transaction processing needs",
            "Complex multi-entity financial consolidation",
        ],
        "processes": ["Financial accounting and consolidation", "Regulatory reporting", "Treasury and risk management"],
        "modules": ["FI", "CO", "Treasury"],
        "integration_requirements": ["Core banking systems", "Regulatory reporting platforms", "Risk management tools"],
        "transformation_opportunities": [
            "Automated regulatory reporting",
            "Real-time financial consolidation",
            "AI-assisted fraud and anomaly detection",
        ],
        "typical_use_cases": [
            "Multi-entity financial close automation",
            "Regulatory capital reporting",
            "Intercompany reconciliation",
        ],
        "related_services": ["sap-security", "sap-data-analytics", "sap-implementation"],
        "faqs": [
            (
                "How do you ensure changes don't compromise audit controls?",
                "Change management follows documented approval and testing steps aligned to your existing audit and controls framework.",
            ),
            (
                "Can this integrate with our core banking platform?",
                "Yes — integration is scoped against your specific core banking and risk systems.",
            ),
        ],
    },
    {
        "slug": "chemicals",
        "name": "Chemicals",
        "short_summary": "Recipe and batch management, EHS compliance, and volatile raw-material cost tracking.",
        "hero_intro": "Chemicals manufacturing combines hazardous material handling, complex recipes, and raw material costs that can shift significantly — SAP has to keep pace with all three.",
        "sap_landscape": "Chemicals manufacturers typically run SAP's process industry capabilities (PP-PI) for recipe and batch management, tightly coupled with EHS compliance and safety data sheet systems.",
        "outcomes": "Operate is central given the safety and compliance burden; Optimize applies through batch yield and raw-material cost management.",
        "cta_label": "Discuss Your Chemicals Challenge",
        "order": 11,
        "challenges": [
            "Hazardous material handling and compliance",
            "Batch and recipe management complexity",
            "Volatile raw material costs",
        ],
        "processes": ["Recipe and batch production management", "Environmental health and safety compliance", "Procurement and pricing"],
        "modules": ["PP-PI (process industries)", "QM", "EHS"],
        "integration_requirements": ["Safety data sheet (SDS) systems", "Environmental reporting platforms", "Supplier pricing feeds"],
        "transformation_opportunities": [
            "Automated EHS compliance reporting",
            "Dynamic raw-material pricing models",
            "Batch yield optimization",
        ],
        "typical_use_cases": [
            "Hazardous material tracking",
            "Batch genealogy for recalls",
            "Environmental incident reporting",
        ],
        "related_services": ["sap-security", "sap-implementation", "sap-data-analytics"],
        "faqs": [
            (
                "Does this cover regulatory reporting for hazardous materials?",
                "Yes — EHS compliance reporting is scoped against the specific regulatory regimes you operate under.",
            ),
            (
                "Can batch genealogy support a product recall scenario?",
                "That's exactly what it's designed for — full genealogy tracking lets you trace a batch forward and backward through production.",
            ),
        ],
    },
    {
        "slug": "technology",
        "name": "Technology",
        "short_summary": "Subscription billing, revenue recognition, and product-to-cash for software and technology companies.",
        "hero_intro": "Technology companies increasingly sell subscriptions and usage-based services — SAP's revenue recognition and billing processes need to match that model, not a traditional one-time-sale process.",
        "sap_landscape": "Technology companies typically run SAP SD alongside Revenue Accounting and Reporting (RAR) for subscription revenue recognition, integrated with cloud billing and usage-metering platforms.",
        "outcomes": "Innovate and Integrate are central here — connecting usage data into billing and revenue recognition tends to be the highest-value work.",
        "cta_label": "Discuss Your Technology Sector Challenge",
        "order": 12,
        "challenges": [
            "Subscription and usage-based revenue recognition",
            "Rapid product and pricing changes",
            "Integration with cloud billing platforms",
        ],
        "processes": ["Subscription billing and revenue recognition", "Product lifecycle management", "Project-based professional services delivery"],
        "modules": ["SD", "RAR (Revenue Accounting and Reporting)", "PS"],
        "integration_requirements": ["Cloud billing platforms", "CRM systems", "Usage and metering data"],
        "transformation_opportunities": [
            "Automated revenue recognition for subscriptions",
            "Real-time usage-based billing",
            "Integrated product-to-cash processes",
        ],
        "typical_use_cases": [
            "Subscription renewal automation",
            "Usage-based invoicing",
            "Multi-element revenue allocation",
        ],
        "related_services": ["sap-data-analytics", "sap-btp", "sap-integration"],
        "faqs": [
            (
                "Can SAP RAR handle complex multi-element subscription bundles?",
                "Yes — RAR is built specifically for multi-element revenue allocation; configuration is scoped around your actual bundle structures.",
            ),
            (
                "Do you integrate with our existing cloud billing platform?",
                "Yes — integration is scoped against whichever billing and metering platform you currently use.",
            ),
        ],
    },
]


class Command(BaseCommand):
    help = "Seeds the 12 industry pages (Section 12) with genuinely industry-specific content."

    @transaction.atomic
    def handle(self, *args, **options):
        for data in INDUSTRIES_DATA:
            industry, created = Industry.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "name": data["name"],
                    "short_summary": data["short_summary"],
                    "hero_intro": data["hero_intro"],
                    "sap_landscape": data["sap_landscape"],
                    "outcomes": data["outcomes"],
                    "cta_label": data["cta_label"],
                    "order": data["order"],
                },
            )

            industry.list_items.all().delete()
            section_keys = (
                (IndustryListItem.CHALLENGES, "challenges"),
                (IndustryListItem.PROCESSES, "processes"),
                (IndustryListItem.MODULES, "modules"),
                (IndustryListItem.INTEGRATION, "integration_requirements"),
                (IndustryListItem.OPPORTUNITIES, "transformation_opportunities"),
                (IndustryListItem.USE_CASES, "typical_use_cases"),
            )
            for section, key in section_keys:
                for index, text in enumerate(data[key]):
                    IndustryListItem.objects.create(industry=industry, section=section, text=text, order=index)

            industry.faqs.all().delete()
            for index, (question, answer) in enumerate(data["faqs"]):
                FAQ.objects.create(content_object=industry, question=question, answer=answer, order=index)

            related = Service.objects.filter(slug__in=data["related_services"])
            industry.related_services.set(related)

            self.stdout.write(f"{'Created' if created else 'Updated'} industry: {industry.name}")

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(INDUSTRIES_DATA)} industries."))
