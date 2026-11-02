from django.test import SimpleTestCase
from django.urls import reverse

# Create your tests here.
class HealthCheckTests(SimpleTestCase):
    def test_health_endpoint_returns_200(self):
        url = reverse("health_check")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_health_endpoint_returns_plain_text(self):
        response = self.client.get("/health/")

        self.assertEqual(response.content, b"health check")
        self.assertEqual(
            response["Content-Type"],
            "text/plain"
        )
