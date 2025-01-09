from django.test import TestCase
from django.shortcuts import reverse


class HomePageTest(TestCase):
    def test_landingpage(self):
        # TODO some sort of test
        response = self.client.get(reverse("landingpage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landingpage.html")

