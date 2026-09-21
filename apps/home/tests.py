"""Tests for the homepage."""

from django.test import TestCase
from wagtail.models import Site
from wagtail.test.utils import WagtailPageTestCase

from apps.home.models import HomePage
from apps.pages.models import StandardPage


class HomePageTests(WagtailPageTestCase):
    def setUp(self):
        self.home = HomePage.objects.first()

    def test_homepage_is_site_root(self):
        site = Site.objects.get(is_default_site=True)
        self.assertEqual(site.root_page.specific, self.home)

    def test_homepage_renders(self):
        response = self.client.get(self.home.url, HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/home_page.html")

    def test_heading_falls_back_to_title(self):
        self.home.hero_heading = ""
        self.assertEqual(self.home.heading, self.home.title)

    def test_only_one_homepage_allowed(self):
        self.assertEqual(HomePage.max_count, 1)

    def test_can_create_standard_page_under_home(self):
        self.assertCanCreateAt(HomePage, StandardPage)

    def test_seo_defaults(self):
        self.home.seo_title = ""
        self.home.og_title = ""
        self.assertEqual(self.home.meta_title, self.home.title)
        self.assertEqual(self.home.social_title, self.home.title)


class BlockRenderingTests(TestCase):
    """Every block must render without raising."""

    def test_all_blocks_render(self):
        import json

        home = HomePage.objects.first()
        home.body = json.dumps(
            [
                {
                    "type": "hero",
                    "value": {
                        "heading": "Hero heading",
                        "subheading": "Hero subheading",
                        "alignment": "center",
                        "buttons": [],
                    },
                },
                {"type": "rich_text", "value": "<p>Some prose.</p>"},
                {
                    "type": "feature_grid",
                    "value": {
                        "heading": "Features",
                        "columns": "3",
                        "cards": [
                            {"icon": "bolt", "title": "Fast", "text": "Very fast.", "link": {}}
                        ],
                    },
                },
                {
                    "type": "call_to_action",
                    "value": {
                        "heading": "Talk to us",
                        "style": "accent",
                        "buttons": [
                            {
                                "text": "Contact",
                                "external_url": "https://example.com",
                                "style": "primary",
                            }
                        ],
                    },
                },
                {
                    "type": "testimonial",
                    "value": {"quote": "Great work.", "author_name": "A. Person"},
                },
                {
                    "type": "stats",
                    "value": {"stats": [{"value": "99%", "label": "Uptime"}]},
                },
                {
                    "type": "faq",
                    "value": {"items": [{"question": "Why?", "answer": "<p>Because.</p>"}]},
                },
            ]
        )
        home.save_revision().publish()

        response = self.client.get(home.url, HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        for needle in [
            "Hero heading",
            "Some prose.",
            "Features",
            "Talk to us",
            "Great work.",
            "Uptime",
            "Because.",
        ]:
            self.assertIn(needle, content)
