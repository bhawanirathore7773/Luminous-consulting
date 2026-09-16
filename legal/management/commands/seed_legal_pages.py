"""
Seeds the 5 legal pages (Section 34) with generic template content.

Bracketed placeholders ([Company Name], [contact email], [jurisdiction])
mark exactly what needs to be filled in with real specifics. Combined with
the visible "not reviewed by legal counsel" banner in the template, this
avoids presenting boilerplate as finished, compliant legal text — which
Claude, not being a lawyer, has no basis to certify anyway.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from legal.models import LegalPage

LEGAL_PAGES_DATA = [
    {
        "slug": "privacy-policy",
        "title": "Privacy Policy",
        "content": (
            'This Privacy Policy explains how [Company Name] ("we," "us," or "our") collects, uses, and '
            "protects information when you visit this website or engage with our services.\n\n"
            "Information we collect\n"
            "We may collect information you provide directly, such as your name, work email, company, job "
            "title, and any details you share through our contact or assessment forms. We may also collect "
            "standard technical information automatically, such as your IP address, browser type, and pages "
            "visited, typically through analytics tools.\n\n"
            "How we use information\n"
            "We use the information you provide to respond to inquiries, follow up on consultation requests, "
            "and improve this website. We do not sell personal information to third parties.\n\n"
            "Cookies\n"
            "This site may use cookies for basic functionality and analytics. See our Cookie Policy for "
            "details.\n\n"
            "Data retention\n"
            "We retain information for as long as necessary to respond to your inquiry or maintain a business "
            "relationship, and in line with applicable law.\n\n"
            "Your rights\n"
            "Depending on your jurisdiction, you may have rights to access, correct, or delete your personal "
            "information. Contact us at [privacy contact email] to make a request.\n\n"
            "Changes to this policy\n"
            "We may update this policy from time to time. The date at the top of this page reflects the most "
            "recent revision."
        ),
    },
    {
        "slug": "terms",
        "title": "Terms of Service",
        "content": (
            'These Terms of Service ("Terms") govern your use of this website, operated by [Company Name]. '
            "By using this site, you agree to these Terms.\n\n"
            "Use of this site\n"
            "This website is provided for informational purposes about our SAP consulting and technology "
            "services. You agree not to misuse this site, attempt unauthorized access to any systems, or use "
            "it in a way that could harm its operation.\n\n"
            "Intellectual property\n"
            "Content on this site, including text, graphics, and design, is owned by [Company Name] or its "
            "licensors and may not be reproduced without permission.\n\n"
            "No professional advice\n"
            "Content on this site, including the SAP assessment tool, is for general informational purposes "
            "only and does not constitute professional consulting advice or a formal system audit. Engaging "
            "our services requires a separate agreement.\n\n"
            "Limitation of liability\n"
            "To the extent permitted by law, [Company Name] is not liable for any indirect, incidental, or "
            "consequential damages arising from your use of this website.\n\n"
            "Governing law\n"
            "These Terms are governed by the laws of [jurisdiction].\n\n"
            "Contact\n"
            "Questions about these Terms can be directed to [contact email]."
        ),
    },
    {
        "slug": "cookie-policy",
        "title": "Cookie Policy",
        "content": (
            "This Cookie Policy explains how [Company Name] uses cookies and similar technologies on this "
            "website.\n\n"
            "What are cookies\n"
            "Cookies are small text files stored on your device that help websites function and collect "
            "information about how they're used.\n\n"
            "How we use cookies\n"
            "We may use strictly necessary cookies required for the site to function, and analytics cookies "
            "to understand how visitors use this site so we can improve it. We do not use cookies for "
            "third-party advertising.\n\n"
            "Managing cookies\n"
            "Most browsers let you control or delete cookies through their settings. Disabling certain "
            "cookies may affect how parts of this site function.\n\n"
            "Changes to this policy\n"
            "We may update this policy periodically. The date at the top of this page reflects the most "
            "recent revision."
        ),
    },
    {
        "slug": "disclaimer",
        "title": "Disclaimer",
        "content": (
            "The information provided on this website, including service descriptions, industry content, "
            "insights articles, and the SAP assessment tool, is for general informational purposes only.\n\n"
            "Not professional advice\n"
            "Nothing on this site constitutes formal SAP consulting advice, a system audit, or a guarantee of "
            "specific outcomes. The SAP health assessment tool in particular produces a directional summary "
            "based on a small number of self-reported answers — it is not an authoritative audit of your SAP "
            "landscape, and should not be relied on as one.\n\n"
            "Representative use cases\n"
            "Case studies on this site are labeled as representative use cases. They describe realistic, "
            "generalized scenarios rather than disclosures of specific client engagements, and are not "
            "intended to guarantee similar results for any particular organization.\n\n"
            'No warranty\n'
            'This site is provided "as is" without warranties of any kind, express or implied, to the extent '
            "permitted by law.\n\n"
            "Contact\n"
            "Questions about this disclaimer can be directed to [contact email]."
        ),
    },
    {
        "slug": "accessibility",
        "title": "Accessibility Statement",
        "content": (
            "[Company Name] is committed to making this website usable by as many people as possible, "
            "including people with disabilities.\n\n"
            "Our approach\n"
            "We aim to follow WCAG 2.2 AA guidelines across this site, including semantic HTML, keyboard "
            "navigation, visible focus states, sufficient color contrast, and support for reduced-motion "
            "preferences.\n\n"
            "Known limitations\n"
            "As with most websites, some areas may not yet fully meet every guideline. We treat accessibility "
            "as an ongoing process rather than a one-time checklist.\n\n"
            "Feedback\n"
            "If you encounter an accessibility barrier on this site, please let us know at [accessibility "
            "contact email] so we can address it."
        ),
    },
]


class Command(BaseCommand):
    help = "Seeds the 5 legal pages (Section 34) with generic, clearly-bracketed template content."

    @transaction.atomic
    def handle(self, *args, **options):
        for data in LEGAL_PAGES_DATA:
            page, created = LegalPage.objects.update_or_create(
                slug=data["slug"],
                defaults={"title": data["title"], "content": data["content"]},
            )
            self.stdout.write(f"{'Created' if created else 'Updated'} legal page: {page.title}")

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(LEGAL_PAGES_DATA)} legal pages."))
