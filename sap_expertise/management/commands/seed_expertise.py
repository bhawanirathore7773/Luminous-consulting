"""
Seeds the SAP Expertise page (Section 13).

Deliberately NOT a copy of the spec's full example list — Section 13 says
"only display expertise that the company actually provides." SuccessFactors,
Ariba, and HCM appear in the spec's example categories but aren't referenced
anywhere in the services/industries content already built, so they're left
out here rather than claimed without backing.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from sap_expertise.models import ExpertiseItem

EXPERTISE_DATA = [
    (ExpertiseItem.PLATFORMS, "S/4HANA"),
    (ExpertiseItem.PLATFORMS, "SAP ECC"),
    (ExpertiseItem.PLATFORMS, "SAP HANA"),
    (ExpertiseItem.PLATFORMS, "SAP BTP"),
    (ExpertiseItem.TECHNOLOGIES, "ABAP"),
    (ExpertiseItem.TECHNOLOGIES, "ABAP Cloud / RAP"),
    (ExpertiseItem.TECHNOLOGIES, "Fiori / Fiori Elements"),
    (ExpertiseItem.TECHNOLOGIES, "UI5"),
    (ExpertiseItem.TECHNOLOGIES, "OData"),
    (ExpertiseItem.TECHNOLOGIES, "SAP BTP Integration Suite"),
    (ExpertiseItem.BUSINESS_APPLICATIONS, "EWM"),
    (ExpertiseItem.BUSINESS_APPLICATIONS, "TM"),
    (ExpertiseItem.FUNCTIONAL_AREAS, "FI"),
    (ExpertiseItem.FUNCTIONAL_AREAS, "CO"),
    (ExpertiseItem.FUNCTIONAL_AREAS, "MM"),
    (ExpertiseItem.FUNCTIONAL_AREAS, "SD"),
    (ExpertiseItem.FUNCTIONAL_AREAS, "PP"),
    (ExpertiseItem.FUNCTIONAL_AREAS, "QM"),
    (ExpertiseItem.FUNCTIONAL_AREAS, "PM"),
    (ExpertiseItem.FUNCTIONAL_AREAS, "PS"),
]


class Command(BaseCommand):
    help = "Seeds the SAP Expertise page (Section 13) with items already referenced elsewhere on the site."

    @transaction.atomic
    def handle(self, *args, **options):
        ExpertiseItem.objects.all().delete()
        for index, (category, name) in enumerate(EXPERTISE_DATA):
            ExpertiseItem.objects.create(category=category, name=name, order=index)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(EXPERTISE_DATA)} expertise items."))
