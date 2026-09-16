"""
Production-oriented legal and website-policy content for Luminous Consulting.

The copy is written for the website's actual current technical setup: Django,
server-side sessions/CSRF protection, contact forms, static assets and no
configured advertising/analytics platform. It avoids invented addresses,
phone numbers, email addresses, clients or legal certifications.

Legal owner should review the text against the final legal entity, contracts,
data flows and jurisdictions before relying on it as legal advice.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from legal.models import LegalPage


LEGAL_PAGES_DATA = [
    {
        "slug": "privacy-policy",
        "title": "Privacy Policy",
        "content": (
            'Privacy Policy\n\n'
            'This Privacy Policy explains how Luminous Consulting ("Luminous", "we", "us" or "our") '
            'handles personal information submitted through this website. It applies to information '
            'provided through enquiry, consultation and assessment forms and to information generated '
            'by normal website operation.\n\n'
            '1. Information we collect\n'
            'You may choose to provide your name, work email, company, job title, country, phone number, '
            'SAP environment, current SAP system, project stage, timeline, estimated scope, requested '
            'services and message content. We also receive technical information that is normally sent '
            'with an HTTP request, such as IP address, browser information, device information, requested '
            'URL and timestamps, where this is available from the hosting and security infrastructure.\n\n'
            '2. Why we use information\n'
            'We use enquiry information to respond to requests, understand a prospective project, '
            'schedule discussions and provide relevant information about SAP services. We may use '
            'technical information to operate, secure, troubleshoot and improve the website. We do not '
            'sell personal information as a commercial data product.\n\n'
            '3. Contact forms and assessment information\n'
            'Information submitted through a form is used for the purpose for which it was submitted. '
            'Please do not send passwords, payment-card numbers, private keys, production credentials, '
            'security tokens or other highly sensitive information through a general website form.\n\n'
            '4. Cookies and similar technologies\n'
            'The current Django application uses cookies required for normal web functionality, including '
            'session handling and CSRF protection. The application is not configured to use advertising '
            'cookies. If analytics, marketing or other non-essential tracking is introduced later, the '
            'website policies and consent experience should be updated before that technology is enabled.\n\n'
            '5. Sharing and service providers\n'
            'Website information may be processed by infrastructure providers that host, secure or operate '
            'the service, and by professional service providers where necessary to respond to a legitimate '
            'business request. Providers should receive only the information needed for their function and '
            'should be subject to appropriate contractual or security controls.\n\n'
            '6. Security\n'
            'The application uses HTTPS-aware security settings, secure cookies in production, CSRF '
            'protection, clickjacking protection, content-type sniffing protection and a restrictive '
            'referrer policy. No internet service can guarantee absolute security, so do not submit '
            'secrets through a public form.\n\n'
            '7. Retention\n'
            'Information is retained only for as long as reasonably necessary for the purpose for which '
            'it was collected, legitimate business administration, security, dispute handling and applicable '
            'legal obligations. Exact retention periods depend on the type of record and the relationship '
            'with the individual or organisation.\n\n'
            '8. Your privacy rights\n'
            'Depending on the law that applies to you, you may have rights concerning access, correction, '
            'deletion, withdrawal of consent, grievance handling or other controls over personal data. '
            'For India, the Digital Personal Data Protection Act, 2023 and the Digital Personal Data '
            'Protection Rules, 2025 provide the relevant statutory framework as their respective provisions '
            'come into force. We will handle valid requests according to applicable law.\n\n'
            '9. International processing\n'
            'Hosting, infrastructure and service providers may process information in countries different '
            'from where you live. Where applicable law imposes requirements for cross-border processing, '
            'those requirements should be considered before processing is arranged.\n\n'
            '10. Children\n'
            'This is a business-to-business consulting website and is not directed to children. Please do '
            'not submit information belonging to a child through a general enquiry form.\n\n'
            '11. Changes\n'
            'We may update this Policy when the website, services, data practices or applicable requirements '
            'change. The date shown on this page indicates the latest seeded/reviewed version.\n\n'
            '12. Privacy requests\n'
            'For a privacy question or request, use the website Contact page and clearly state that the '
            'request concerns privacy or personal data. We may need reasonable information to verify and '
            'process the request.'
        ),
    },
    {
        "slug": "terms",
        "title": "Terms of Service",
        "content": (
            'Website Terms of Service\n\n'
            'These Terms describe the basic rules for using the Luminous Consulting website. They apply to '
            'the website itself. A signed proposal, statement of work, master services agreement or other '
            'client contract governs the delivery of consulting services where it contains different or '
            'additional terms.\n\n'
            '1. Website purpose\n'
            'The website provides information about SAP consulting, implementation, integration, development, '
            'data, security, testing and managed services. Website content is general information and is not '
            'a substitute for a project-specific technical, legal, security, tax or financial assessment.\n\n'
            '2. Acceptable use\n'
            'You may use the website for lawful business and informational purposes. You must not attempt '
            'unauthorised access, interfere with availability or security, introduce malicious code, scrape '
            'protected areas, impersonate another person or organisation, or use the website to violate '
            'applicable law.\n\n'
            '3. Consulting enquiries\n'
            'Submitting an enquiry does not create a consulting engagement, guarantee availability or create '
            'a contract. A consulting relationship begins only when the applicable commercial agreement is '
            'accepted by the relevant parties.\n\n'
            '4. Website content and intellectual property\n'
            'Unless otherwise stated, website text, original graphics, page layouts, branding and software '
            'code are owned by or licensed to Luminous Consulting. Third-party names, trademarks, product '
            'names and customer stories remain the property of their respective owners. You may view and '
            'share ordinary website links, but you may not reproduce substantial proprietary content for '
            'commercial redistribution without permission.\n\n'
            '5. SAP and third-party references\n'
            'SAP, S/4HANA, SAP BTP and other SAP product names are trademarks or registered trademarks of '
            'SAP SE or its affiliates. Luminous Consulting is independently operated unless expressly stated '
            'otherwise. Third-party customer stories shown for context are attributed to their original '
            'publishers and are not representations that those organisations are Luminous clients.\n\n'
            '6. Accuracy and availability\n'
            'We aim to keep information useful and current, but service descriptions, technology capabilities '
            'and external links can change. The website may occasionally be unavailable for maintenance, '
            'security work or reasons outside our control.\n\n'
            '7. No guarantee of outcomes\n'
            'Examples and representative use cases describe possible delivery patterns. They do not promise '
            'a particular financial, operational, technical or compliance result for any organisation. '
            'Project outcomes depend on scope, systems, data, governance, people, third-party services and '
            'other factors.\n\n'
            '8. External websites\n'
            'The website may link to official SAP pages or other external resources. We do not control those '
            'websites and their own terms and privacy policies apply.\n\n'
            '9. Liability\n'
            'To the maximum extent permitted by applicable law, the website is provided for general '
            'informational use and Luminous Consulting does not make an unrestricted warranty that it will '
            'always be error-free, uninterrupted or suitable for every purpose. Nothing in these website '
            'terms excludes liability that cannot lawfully be excluded. Client-specific liability, warranties '
            'and remedies are governed by the applicable signed agreement.\n\n'
            '10. Governing terms\n'
            'These website terms do not replace a signed client agreement and do not attempt to create a '
            'governing-law clause where none has been expressly established. Where you engage Luminous '
            'Consulting under a written agreement, the governing-law and dispute provisions of that agreement '
            'apply.\n\n'
            '11. Changes\n'
            'We may update these Terms when the website or services change. Continued use after an update '
            'means the updated website terms are available for review.\n\n'
            '12. Contact\n'
            'For questions about these website terms, use the Contact page.'
        ),
    },
    {
        "slug": "cookie-policy",
        "title": "Cookie Policy",
        "content": (
            'Cookie Policy\n\n'
            'This Cookie Policy explains the cookies used by the current Luminous Consulting website. '
            'A cookie is a small piece of data stored by a browser for a website. Cookies can be essential '
            'to security, sessions and user preferences.\n\n'
            '1. Essential cookies\n'
            'The Django application uses a session cookie to support server-side sessions and a CSRF cookie '
            'to help protect form submissions against cross-site request forgery. These cookies are functional '
            'rather than advertising cookies.\n\n'
            '2. Security-related settings\n'
            'In production the application is configured to use secure and HTTP-only cookie settings where '
            'supported by the browser. These controls reduce the risk of cookies being read by client-side '
            'scripts or transmitted over an insecure connection.\n\n'
            '3. Analytics and advertising\n'
            'The current application code does not intentionally configure an advertising-cookie system or '
            'a third-party analytics platform. If such a service is added, its purpose, provider, cookie '
            'categories, retention and consent requirements should be documented before activation.\n\n'
            '4. Third-party content\n'
            'The website currently loads the Inter font from Google Fonts and Alpine.js from jsDelivr. '
            'These are third-party network resources; their providers may process connection information '
            'according to their own policies. A future production deployment can self-host these assets if '
            'a stricter third-party dependency model is required.\n\n'
            '5. Managing cookies\n'
            'You can delete or restrict cookies through your browser settings. Blocking essential cookies '
            'may prevent contact forms, sessions or other parts of the website from working correctly.\n\n'
            '6. Changes\n'
            'This Policy will be updated if the website introduces new cookies, analytics, advertising or '
            'other tracking technologies.\n\n'
            '7. Contact\n'
            'For a question about cookies or tracking on this website, use the Contact page.'
        ),
    },
    {
        "slug": "disclaimer",
        "title": "Disclaimer",
        "content": (
            'Website Disclaimer\n\n'
            'The information on this website is provided for general business and technology information. '
            'It describes SAP consulting capabilities, possible delivery approaches, technology concepts, '
            'representative scenarios and publicly attributed third-party customer stories.\n\n'
            '1. Not professional advice\n'
            'Website content is not a formal SAP system audit, legal opinion, tax opinion, financial advice, '
            'security certification or project-specific implementation plan. A project should be assessed '
            'against the customer landscape, requirements, data, contracts and applicable controls before '
            'technical decisions are made.\n\n'
            '2. Representative use cases\n'
            'Pages labelled representative use case describe generalized scenarios. They are not presented '
            'as undisclosed client engagements and should not be interpreted as proof of a specific Luminous '
            'customer result.\n\n'
            '3. Public customer stories\n'
            'Where the website references SAP customer stories, the customer, results and statements belong '
            'to the original publisher and are presented with attribution. Such references are provided as '
            'industry context and do not imply that the named organisation is a Luminous Consulting client.\n\n'
            '4. Technology information\n'
            'SAP product names, cloud services, APIs, frameworks and other technologies can change. Always '
            'confirm current product capabilities and licensing with the relevant vendor before making a '
            'commercial or architectural decision.\n\n'
            '5. External links\n'
            'Links to third-party websites are provided for reference. Luminous Consulting does not control '
            'their content, availability, security or privacy practices.\n\n'
            '6. No guarantee\n'
            'Business results depend on circumstances specific to each organisation. Examples on this website '
            'are not guarantees of cost savings, performance, implementation time, compliance or other outcomes.\n\n'
            '7. Contact\n'
            'For clarification about website content, use the Contact page.'
        ),
    },
    {
        "slug": "accessibility",
        "title": "Accessibility Statement",
        "content": (
            'Accessibility Statement\n\n'
            'Luminous Consulting aims to make this website usable by people with different abilities and '
            'assistive technologies. We use the Web Content Accessibility Guidelines (WCAG) 2.2 as a design '
            'reference, including its principles for perceivable, operable, understandable and robust content.\n\n'
            '1. Accessibility practices\n'
            'The website uses semantic HTML where practical, labelled navigation controls, keyboard-focus '
            'styles, a skip-to-content link, responsive layouts, descriptive link text and reduced-motion '
            'support for the primary animated interface element. The mobile navigation can be operated with '
            'keyboard controls on devices that provide a keyboard and can be closed with Escape.\n\n'
            '2. Current status\n'
            'Accessibility is an ongoing engineering process. This statement is not a claim of independent '
            'WCAG certification or verified conformance. Pages, third-party resources and future content '
            'should continue to be tested as the site changes.\n\n'
            '3. Known considerations\n'
            'Third-party resources, browser differences, newly published content and external documents may '
            'create accessibility issues outside the control of a single page template. We aim to identify '
            'and correct barriers as they are reported.\n\n'
            '4. Feedback\n'
            'If you cannot access a page, control, form or document, use the Contact page and describe the '
            'problem, the page URL and the device or assistive technology involved if you are comfortable '
            'sharing it. We will use the information to investigate and improve the experience.\n\n'
            '5. Accessibility standard\n'
            'WCAG 2.2 is an international W3C accessibility standard. The site uses it as a development '
            'reference; the presence of this statement should not be interpreted as a formal certification.'
        ),
    },
]


class Command(BaseCommand):
    help = "Seed the website's legal and policy pages."

    @transaction.atomic
    def handle(self, *args, **options):
        for data in LEGAL_PAGES_DATA:
            page, created = LegalPage.objects.update_or_create(
                slug=data["slug"],
                defaults={"title": data["title"], "content": data["content"]},
            )
            self.stdout.write(f"{'Created' if created else 'Updated'} legal page: {page.title}")

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(LEGAL_PAGES_DATA)} legal pages."))
