from django.test import TestCase
from django.urls import reverse


class SmokeTests(TestCase):
    def test_health_endpoint(self):
        response = self.client.get(reverse("core:healthz"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_homepage_loads(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Make SAP simpler. Make the business faster.")
        self.assertContains(response, "Data & Analytics")
        self.assertContains(response, "Public SAP customer stories")

    def test_approach_page_loads(self):
        response = self.client.get(reverse("core:approach"))
        self.assertEqual(response.status_code, 200)

    def test_robots_txt_loads(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Sitemap:", response.content.decode())

    def test_mobile_navigation_markup_exists(self):
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, 'id="mobile-navigation"')
        self.assertContains(response, 'mobileOpen = !mobileOpen')
        self.assertContains(response, "translate-x-full")

    def test_home_seo_metadata_exists(self):
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, 'name="description"')
        self.assertContains(response, 'rel="canonical"')
        self.assertContains(response, 'application/ld+json')
