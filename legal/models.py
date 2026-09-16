from django.db import models


class LegalPage(models.Model):
    """
    Section 34. Seeded content is a generic starting template, not
    jurisdiction-reviewed legal text — Claude isn't a lawyer, and the spec
    itself calls for this to be "configurable" rather than hardcoded, so
    it's a normal admin-editable model rather than static templates.
    """

    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=150)
    content = models.TextField()
    last_updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
