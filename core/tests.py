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

    def test_approach_page_loads(self):
        response = self.client.get(reverse("core:approach"))
        self.assertEqual(response.status_code, 200)

    def test_robots_txt_loads(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Sitemap:", response.content.decode())
