"""
Seeds 6 insights articles (Section 21) spanning distinct categories and
content types, so search and category filtering both have something real
to demonstrate. Content is genuine SAP domain knowledge written for this
site — no fabricated statistics, quotes, or client references.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from insights.models import Article
from services.models import Service

ARTICLES_DATA = [
    {
        "slug": "why-brownfield-s4hana-conversions-stall",
        "title": "Why Brownfield S/4HANA Conversions Stall Midway",
        "summary": "The technical conversion usually isn't what stalls a brownfield project — the custom code decisions made in the first few weeks are.",
        "category": Article.S4HANA,
        "content_type": Article.ARTICLE,
        "published_date": "2026-08-01",
        "cta_label": "Discuss Your S/4HANA Conversion",
        "content": (
            "Most brownfield S/4HANA conversions don't stall because the technical conversion tooling fails. "
            "They stall because of decisions made — or deferred — in the first few weeks of the project, "
            "specifically around custom code.\n\n"
            "A typical ECC landscape carries years of custom reports, enhancements, and modifications, not all "
            "of which are still in active use. Before conversion, it's common to discover that a meaningful "
            "share of that custom code hasn't been touched in years, some of it superseded by standard "
            "S/4HANA functionality that didn't exist when it was written.\n\n"
            "The mistake teams make is treating custom code remediation as a single technical checklist item "
            "rather than a business decision. Every custom object needs an owner who can say whether it's "
            "still needed, and in what form. Without that ownership, remediation work either stalls waiting "
            "for answers, or worse, code gets carried forward unchanged simply because no one wanted to be "
            "the one to say it could be retired.\n\n"
            "The projects that move smoothly through this phase run the custom code assessment early — "
            "ideally before the conversion timeline is even finalized — and get business sign-off on a "
            "disposition for each object: retire, replace with standard functionality, or remediate. That "
            "decision-making, not the technical migration itself, is usually the actual critical path."
        ),
        "related_services": ["sap-s4hana", "sap-development"],
        "order": 1,
    },
    {
        "slug": "sap-integration-architecture-review-checklist",
        "title": "A Practical Checklist for SAP Integration Architecture Reviews",
        "summary": "Six questions worth asking before adding another interface to an already-complex SAP integration landscape.",
        "category": Article.INTEGRATION,
        "content_type": Article.CHECKLIST,
        "published_date": "2026-07-15",
        "cta_label": "Discuss Your Integration Architecture",
        "content": (
            "Before building another point-to-point interface into an already-complex SAP landscape, it's "
            "worth running through a short set of questions. None of these require special tooling — just an "
            "honest look at what's actually there.\n\n"
            "Does anyone have a current diagram of every interface touching SAP? If the answer is no, or the "
            "diagram is more than a year old, that's usually the first problem to fix, before adding anything "
            "new.\n\n"
            "Is there a single place to see when an integration last ran successfully? Point-to-point "
            "interfaces without centralized monitoring tend to fail silently, and the first sign of trouble "
            "is often a business user noticing missing data days later.\n\n"
            "Does each interface have an owner who understands what it does? Interfaces built by contractors "
            "or long-departed staff, with no documentation and no clear owner, are a common source of risk "
            "during any subsequent change.\n\n"
            "Would a new interface reuse an existing integration pattern, or introduce a new one? Every new "
            "pattern — a new protocol, a new middleware tool, a new authentication method — adds to what the "
            "team needs to maintain going forward.\n\n"
            "Is the interface idempotent, and does it handle retries? Interfaces that assume every message "
            "arrives exactly once tend to cause data problems the first time a network hiccup causes a "
            "retry.\n\n"
            "Finally, what happens if this interface goes down for a day? If the answer is \"no one would "
            "notice until it caused a bigger problem downstream,\" monitoring and alerting probably need "
            "attention before the interface count grows any further."
        ),
        "related_services": ["sap-integration"],
        "order": 2,
    },
    {
        "slug": "clean-core-sap-btp-in-practice",
        "title": "Clean Core on SAP BTP: What It Actually Means in Practice",
        "summary": "Clean core isn't a rule against writing any custom code — it's a rule about where that code lives and how it survives an upgrade.",
        "category": Article.BTP,
        "content_type": Article.GUIDE,
        "published_date": "2026-06-20",
        "cta_label": "Talk Through Your Clean Core Approach",
        "content": (
            "\"Clean core\" gets used loosely enough that it's worth being specific about what it actually "
            "means in practice, since the term is sometimes misread as \"no custom code at all.\"\n\n"
            "The actual principle is narrower: keep the S/4HANA core system as close to standard SAP as "
            "possible, and put custom logic somewhere that doesn't get touched by an upgrade. In practice, "
            "that means SAP BTP rather than the core ABAP stack — extensions built via the Cloud Application "
            "Programming Model, side-by-side extensions, or in-app extensions using released APIs rather than "
            "direct table access or core object modifications.\n\n"
            "The reason this matters isn't philosophical. It's operational: every custom modification inside "
            "the core system is something that has to be re-tested, and sometimes re-written, at the next "
            "upgrade. A landscape with years of core modifications tends to make S/4HANA upgrades "
            "progressively more expensive and risky over time, which is often what eventually forces an "
            "organization into exactly the kind of high-risk, compressed conversion project that could have "
            "been avoided.\n\n"
            "Getting clean core right isn't just a technology choice — it needs governance. Someone needs to "
            "own the decision about when a requirement genuinely needs custom development versus when it can "
            "be met with standard configuration or a business process change instead. Without that "
            "governance, BTP extensions can accumulate the same kind of technical debt custom ABAP always "
            "did — it's just moved to a different platform, not eliminated."
        ),
        "related_services": ["sap-btp", "sap-development"],
        "order": 3,
    },
    {
        "slug": "segregation-of-duties-sap-security-basics",
        "title": "Segregation of Duties: The SAP Security Basics Most Teams Skip",
        "summary": "Most segregation-of-duties conflicts aren't caused by malicious intent — they're caused by roles that grew without anyone reviewing the combination.",
        "category": Article.SECURITY,
        "content_type": Article.ARTICLE,
        "published_date": "2026-05-10",
        "cta_label": "Review Your SAP Authorizations",
        "content": (
            "Segregation-of-duties conflicts in SAP rarely come from anyone trying to do something wrong. "
            "They come from roles that accumulated permissions over years, one reasonable-sounding access "
            "request at a time, until a single user ends up able to both create a vendor and approve payment "
            "to that vendor without anyone noticing the combination.\n\n"
            "The basic principle is straightforward: no single person should hold both sides of a critical "
            "control — creating and approving, ordering and receiving, or entering and reconciling. The "
            "difficulty is almost never understanding the principle. It's the sheer number of transaction and "
            "authorization object combinations in a mature SAP landscape, which makes manual review "
            "impractical past a certain organization size.\n\n"
            "The teams that manage this well don't try to catch every conflict through periodic manual "
            "audits. They build the check into how role changes get approved in the first place — a proposed "
            "authorization change gets run against known conflict rules before it goes live, not discovered "
            "months later during an annual review.\n\n"
            "It's also worth separating genuine risk from theoretical risk. Not every technical "
            "segregation-of-duties conflict represents a real business risk — a small finance team may have "
            "no practical way to fully separate certain duties, and the right mitigation might be a "
            "compensating control, like a monthly reconciliation review, rather than a role redesign that "
            "isn't operationally realistic. The goal is a defensible, risk-based process, not a zero-conflict "
            "role model that no one can actually work within."
        ),
        "related_services": ["sap-security"],
        "order": 4,
    },
    {
        "slug": "consolidating-sap-reporting-without-overhaul",
        "title": "Consolidating SAP Reporting Without a Full Data Platform Overhaul",
        "summary": "Inconsistent numbers across departments are usually a data model problem, not a reason to replace every reporting tool at once.",
        "category": Article.DATA_ANALYTICS,
        "content_type": Article.GUIDE,
        "published_date": "2026-04-05",
        "cta_label": "Discuss Your Reporting Consolidation",
        "content": (
            "When departmental reports don't match at the executive level, the instinctive response is often "
            "to propose replacing every reporting tool with one new platform. That's rarely the fastest or "
            "cheapest fix, and it's not always necessary.\n\n"
            "In most cases, inconsistent numbers come from each department building its own extraction logic "
            "against the same underlying SAP tables, with slightly different filters, date logic, or currency "
            "conversion assumptions. The fix isn't a new visualization tool — it's a single, well-documented "
            "data model that every report pulls from, so the inconsistency is designed out rather than "
            "reconciled after the fact.\n\n"
            "Building that consolidated model doesn't require ripping out every existing dashboard. It "
            "usually means defining canonical definitions for the metrics that actually cause disagreement — "
            "revenue recognition timing, what counts as an \"open\" order, how intercompany transactions get "
            "treated — and exposing those definitions through a shared semantic layer that existing tools can "
            "connect to.\n\n"
            "Where a platform like SAP Datasphere earns its place is in providing that shared layer without "
            "requiring every report to be rebuilt from scratch on day one. Reports can migrate to the "
            "consolidated model incrementally, which also means the organization sees value — consistent "
            "numbers — well before the full migration is complete, rather than waiting for a single big-bang "
            "cutover."
        ),
        "related_services": ["sap-data-analytics"],
        "order": 5,
    },
    {
        "slug": "where-ai-actually-helps-in-sap",
        "title": "Where AI Actually Helps in an SAP Landscape (and Where It Doesn't Yet)",
        "summary": "The AI use cases that stick tend to be narrow, high-volume, and boring — not the broad, open-ended ones that get pitched first.",
        "category": Article.AI,
        "content_type": Article.ARTICLE,
        "published_date": "2026-03-12",
        "cta_label": "Explore AI Use Cases for SAP",
        "content": (
            "The AI use cases that actually make it to production in an SAP landscape tend to look "
            "unglamorous next to the ones that get pitched in a strategy workshop. They're narrow, "
            "high-volume, and often invisible to anyone outside the team that benefits from them.\n\n"
            "Document processing is a good example — extracting structured data from incoming invoices or "
            "purchase orders and matching it against existing records. It's not a novel idea, but it's "
            "high-volume, rules-adjacent, and has a clear, measurable outcome: fewer manual entries, faster "
            "matching, fewer exceptions.\n\n"
            "Anomaly detection on transactional data is another. Flagging unusual payment patterns, "
            "duplicate vendor records, or out-of-pattern journal entries doesn't require a general-purpose AI "
            "system — it requires a model trained on a well-defined, narrow question, sitting on top of "
            "clean underlying data.\n\n"
            "Where AI use cases tend to stall is the opposite pattern: broad, open-ended initiatives — \"use "
            "AI to improve decision-making across the business\" — that lack a specific, measurable target "
            "and a clean data foundation to build on. Ambitious framing doesn't fix inconsistent master data "
            "or a reporting layer that three departments already don't trust.\n\n"
            "The practical starting point is usually the same regardless of the specific use case: pick "
            "something narrow enough to have an obvious before-and-after measure, make sure the underlying "
            "data is actually clean enough to trust, and treat the AI model as the last step in that process "
            "rather than a shortcut past it."
        ),
        "related_services": ["sap-data-analytics", "sap-btp"],
        "order": 6,
    },
]


class Command(BaseCommand):
    help = "Seeds 6 insights articles (Section 21) across distinct categories and content types."

    @transaction.atomic
    def handle(self, *args, **options):
        for data in ARTICLES_DATA:
            article, created = Article.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "title": data["title"],
                    "summary": data["summary"],
                    "category": data["category"],
                    "content_type": data["content_type"],
                    "published_date": data["published_date"],
                    "cta_label": data["cta_label"],
                    "content": data["content"],
                    "order": data["order"],
                },
            )
            related = Service.objects.filter(slug__in=data["related_services"])
            article.related_services.set(related)
            self.stdout.write(f"{'Created' if created else 'Updated'} article: {article.title}")

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(ARTICLES_DATA)} articles."))
