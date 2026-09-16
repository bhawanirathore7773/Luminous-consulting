"""
Seed the website's legal and policy pages with website-specific content.

The copy reflects the current application architecture and should be reviewed
by qualified counsel before the business begins relying on it as a contractual
or jurisdiction-specific legal notice.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from legal.models import LegalPage


LEGAL_PAGES_DATA = [
    {
        "slug": "privacy-policy",
        "title": "Privacy Policy",
        "content": (
            "Luminous Consulting Privacy Policy\n\n"
            "Effective date\n"
            "September 16, 2026\n\n"
            "1. Scope\n"
            "This Privacy Policy explains how Luminous Consulting handles personal information submitted "
            "through this website, including the contact and SAP assessment flows. It applies to information "
            "provided directly by visitors and to limited technical information needed to operate, secure, "
            "and improve the website. Luminous Consulting is referred to as “Luminous”, “we”, “us”, or “our”.\n\n"
            "2. Information we receive\n"
            "When you use the contact form, we may receive your name, work email, company, job title, country, "
            "phone number, SAP environment, current SAP system details, requested services, project stage, "
            "timeline, estimated scope, and message. The application also records the source of the inquiry "
            "and the date and time it was submitted. Please do not submit passwords, payment-card data, "
            "production credentials, confidential SAP system exports, or other information that is not needed "
            "to discuss an engagement.\n\n"
            "3. How we use information\n"
            "We use submitted information to respond to enquiries, understand the requested SAP service or "
            "project scope, arrange discussions, provide requested information, operate the assessment flow, "
            "protect the website, and maintain business records where appropriate. We do not use the contact "
            "form as a substitute for a secure client system or production incident channel.\n\n"
            "4. Hosting, security and service providers\n"
            "The website is a Django application and may be hosted on infrastructure such as Render or another "
            "hosting provider selected by the site operator. Infrastructure providers may process technical "
            "information such as IP addresses, request metadata, timestamps, browser information, and security "
            "logs as part of delivering and protecting the service. Access to lead information should be limited "
            "to people who need it for legitimate business purposes.\n\n"
            "5. Third-party resources\n"
            "The current website loads the Inter font from Google Fonts and Alpine.js from jsDelivr. These are "
            "external resources requested by the visitor’s browser. Their operators may receive network request "
            "information as described in their own policies. The website currently does not describe itself as "
            "using a third-party advertising network or selling personal information.\n\n"
            "6. Cookies and similar technologies\n"
            "The application may use strictly necessary cookies or browser storage required by Django and the "
            "website’s interactive navigation. This policy does not claim that optional analytics or advertising "
            "cookies are active unless they are actually configured. See the Cookie Policy for details.\n\n"
            "7. Data retention\n"
            "Contact and assessment information is retained for as long as reasonably necessary to respond to "
            "the enquiry, manage an actual or prospective business relationship, maintain business records, "
            "resolve disputes, and meet applicable legal obligations. Retention periods may vary by the nature "
            "of the information and the relationship.\n\n"
            "8. Sharing\n"
            "We may share information with service providers who help host, secure, maintain, or operate the "
            "website, and where disclosure is required by law or necessary to protect rights, safety, security, "
            "or the integrity of the service. We do not sell personal information as a business model.\n\n"
            "9. Your choices and requests\n"
            "Where applicable law gives you rights over your personal information, you may request access, "
            "correction, deletion, restriction, or other available rights. Use the Contact page on this website "
            "to submit a request and provide enough information for us to understand what you are asking for. "
            "We may need to verify a request before acting on it.\n\n"
            "10. International processing\n"
            "Because the website and its infrastructure may use service providers in different countries, "
            "information submitted through the website may be processed outside your country, subject to the "
            "requirements that apply to the relevant processing.\n\n"
            "11. Children\n"
            "This website is intended for business and professional audiences and is not directed to children.\n\n"
            "12. Changes\n"
            "We may update this Privacy Policy when the website, services, or applicable requirements change. "
            "The effective date above identifies the current published version."
        ),
    },
    {
        "slug": "terms",
        "title": "Terms of Use",
        "content": (
            "Luminous Consulting Terms of Use\n\n"
            "Effective date\n"
            "September 16, 2026\n\n"
            "1. About these Terms\n"
            "These Terms govern access to and use of the Luminous Consulting website. The website provides "
            "information about SAP consulting, transformation, implementation, integration, development, data, "
            "security, testing, and managed services. A client engagement is governed by the separate commercial "
            "agreement, statement of work, or other contract signed for that engagement.\n\n"
            "2. Acceptable use\n"
            "You may use this website for lawful business and informational purposes. You must not attempt to "
            "gain unauthorized access, interfere with the availability or security of the website, introduce "
            "malicious code, scrape or copy content in a way that violates applicable law, impersonate another "
            "person or organization, or use the site to submit information you are not authorized to share.\n\n"
            "3. Website content\n"
            "Service descriptions, technology references, insights, representative use cases, and other content "
            "are provided to help visitors understand Luminous Consulting’s capabilities. They are not a promise "
            "that a particular feature, consultant, technology, delivery date, or outcome will be available in "
            "every engagement. Project scope, deliverables, assumptions, fees, timelines, warranties, and service "
            "levels are agreed separately with the client.\n\n"
            "4. Representative use cases\n"
            "Pages labelled as representative use cases are generalized scenarios. They are not disclosures of "
            "specific Luminous Consulting client engagements. Public SAP customer stories are separately attributed "
            "to SAP and are not represented as Luminous Consulting customers.\n\n"
            "5. Intellectual property\n"
            "Unless stated otherwise, website text, layout, original graphics, code, and other materials created "
            "for this website belong to Luminous Consulting or their respective licensors. SAP names, products, "
            "logos, and other third-party marks remain the property of their respective owners. Nothing on this "
            "website grants a licence to use a third-party trademark.\n\n"
            "6. SAP relationship and trademarks\n"
            "Luminous Consulting is independently operated. SAP, SAP S/4HANA, SAP BTP, and other SAP names and "
            "marks referenced on this website are trademarks or registered trademarks of SAP SE or an SAP affiliate "
            "company, as applicable. No statement on this website should be read as creating an SAP partnership, "
            "endorsement, certification, or authorization unless a separate official agreement or designation says so.\n\n"
            "7. External links\n"
            "The website may link to external resources, including SAP-published material. External sites are "
            "operated by their respective owners and are subject to their own terms and privacy practices. A link "
            "does not by itself mean that Luminous Consulting endorses every statement or service on the linked site.\n\n"
            "8. No professional or system warranty\n"
            "Website information is general information. It is not a system audit, security certification, legal "
            "opinion, tax opinion, or binding SAP implementation recommendation. Decisions affecting production "
            "SAP systems should be made using appropriate technical, security, business, and legal review.\n\n"
            "9. Changes and availability\n"
            "We may change, suspend, or remove website content or functionality. We aim to keep information useful "
            "and accurate, but we do not promise that every page will always be complete, current, uninterrupted, "
            "or free from errors.\n\n"
            "10. Contact and engagement terms\n"
            "Questions about the website can be submitted through the Contact page. Any paid services, consulting "
            "deliverables, confidentiality obligations, data-processing terms, warranties, liability provisions, "
            "and governing-law provisions are established in the applicable client agreement rather than by these "
            "website Terms alone."
        ),
    },
    {
        "slug": "cookie-policy",
        "title": "Cookie Policy",
        "content": (
            "Luminous Consulting Cookie Policy\n\n"
            "Effective date\n"
            "September 16, 2026\n\n"
            "1. What cookies are\n"
            "Cookies are small pieces of information stored by a browser. Websites use them for functions such "
            "as maintaining a session, protecting forms, remembering preferences, and understanding usage.\n\n"
            "2. Necessary website cookies\n"
            "Because this website is built with Django, the application may use strictly necessary cookies for "
            "security and session-related functionality. These cookies support normal operation rather than "
            "serving behavioural advertising.\n\n"
            "3. Navigation state\n"
            "The mobile navigation uses client-side JavaScript to open and close the menu and to prevent the page "
            "from scrolling while the drawer is open. The current implementation does not require an advertising "
            "cookie to perform that interaction.\n\n"
            "4. Third-party resources\n"
            "The current website requests Inter font files from Google Fonts and Alpine.js from jsDelivr. These "
            "resources are not cookies set by Luminous, but the browser may send ordinary network information when "
            "requesting them. Their operators publish their own terms and privacy information.\n\n"
            "5. Analytics and advertising\n"
            "The current website should not be described as running optional analytics or targeted advertising "
            "cookies unless those services are actually added to the application. If optional analytics, marketing "
            "tags, or advertising technologies are introduced, this policy and the consent experience should be "
            "updated before they are activated where consent is required.\n\n"
            "6. Browser controls\n"
            "Most modern browsers allow you to inspect, block, or delete cookies. Blocking necessary cookies may "
            "cause parts of the website to stop working correctly.\n\n"
            "7. Updates\n"
            "We may update this Cookie Policy when the technologies used by the website change. The effective date "
            "above identifies the current published version."
        ),
    },
    {
        "slug": "disclaimer",
        "title": "Disclaimer",
        "content": (
            "Luminous Consulting Website Disclaimer\n\n"
            "Effective date\n"
            "September 16, 2026\n\n"
            "1. General information\n"
            "The information on this website is provided for general business and technology information. "
            "Descriptions of SAP services, architectures, implementation approaches, and outcomes are illustrative "
            "unless a page expressly identifies a verified external source.\n\n"
            "2. No guaranteed outcome\n"
            "Technology projects depend on the client’s systems, data, people, governance, scope, dependencies, "
            "vendors, and decisions. Nothing on this website guarantees a particular cost saving, implementation "
            "time, performance improvement, migration result, security posture, or business outcome.\n\n"
            "3. Representative scenarios\n"
            "Representative use cases are generalized examples intended to explain how a service may be applied. "
            "They should not be interpreted as confidential client disclosures or as evidence of a specific client "
            "engagement.\n\n"
            "4. Public SAP references\n"
            "Where this website links to or quotes a public SAP customer story, the customer, quote, and project "
            "description are attributed to the SAP-published source. Such references are not presented as Luminous "
            "Consulting client work.\n\n"
            "5. Assessment tool\n"
            "Any SAP assessment or questionnaire on this website produces a directional summary based on the "
            "information entered by the visitor. It is not an SAP-certified audit, penetration test, compliance "
            "assessment, or substitute for a detailed professional review.\n\n"
            "6. Third-party trademarks\n"
            "SAP and other third-party names, products, and marks remain the property of their respective owners. "
            "Reference to a product or technology does not by itself indicate sponsorship, endorsement, partnership, "
            "certification, or authorization.\n\n"
            "7. External information\n"
            "External links are provided for convenience and source attribution. Luminous Consulting does not "
            "control third-party websites and cannot guarantee their availability, accuracy, or continued content.\n\n"
            "8. Professional review\n"
            "Before making material production, security, compliance, contractual, or financial decisions, obtain "
            "the appropriate technical, business, security, and legal review for your organization."
        ),
    },
    {
        "slug": "accessibility",
        "title": "Accessibility Statement",
        "content": (
            "Luminous Consulting Accessibility Statement\n\n"
            "Effective date\n"
            "September 16, 2026\n\n"
            "1. Our commitment\n"
            "Luminous Consulting aims to make this website usable by people with different abilities, devices, "
            "and input methods. We use semantic HTML, responsive layouts, keyboard-accessible controls, visible "
            "focus states, descriptive link text, sufficient contrast, and reduced-motion support where practical.\n\n"
            "2. Navigation\n"
            "The mobile navigation provides a labelled menu button, an explicit open and close state, an overlay "
            "that can be dismissed by tapping outside the drawer, Escape-key support, and links that close the "
            "drawer after navigation. Interactive controls are designed with touch-friendly target sizes.\n\n"
            "3. Keyboard and focus\n"
            "Interactive controls should remain reachable by keyboard and display a visible focus indication. "
            "We avoid using colour as the only way to communicate an interaction state.\n\n"
            "4. Motion\n"
            "The site uses limited animation for interface transitions and visual flow elements. Where possible, "
            "the interface respects the user’s prefers-reduced-motion setting.\n\n"
            "5. Known limitations\n"
            "Accessibility is an ongoing engineering process. Some third-party resources, browser behaviours, or "
            "content supplied by external services may not be fully controlled by Luminous Consulting. We continue "
            "to test responsive layouts, keyboard navigation, focus behaviour, colour contrast, and touch interaction.\n\n"
            "6. Feedback\n"
            "If you encounter a barrier, please use the Contact page and describe the page, device/browser, and "
            "interaction that caused the problem. We will use that information to investigate and improve the site.\n\n"
            "7. Standards reference\n"
            "Our accessibility approach is informed by the Web Content Accessibility Guidelines (WCAG), including "
            "WCAG 2.2 principles for navigation, focus, input modalities, and responsive use. This statement is "
            "not a claim of formal third-party accessibility certification."
        ),
    },
]


class Command(BaseCommand):
    help = "Seeds website-specific legal and policy pages."

    @transaction.atomic
    def handle(self, *args, **options):
        for data in LEGAL_PAGES_DATA:
            page, created = LegalPage.objects.update_or_create(
                slug=data["slug"],
                defaults={"title": data["title"], "content": data["content"]},
            )
            self.stdout.write(f"{'Created' if created else 'Updated'} legal page: {page.title}")

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(LEGAL_PAGES_DATA)} legal pages."))
