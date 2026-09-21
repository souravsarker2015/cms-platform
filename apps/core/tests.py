"""Tests for shared blocks, snippets and the context processor."""

from django.test import TestCase
from wagtail.models import Site

from apps.core.blocks import BodyStreamBlock, ButtonBlock
from apps.core.models import (
    Footer,
    FooterColumn,
    FooterLink,
    NavigationMenu,
    NavigationMenuItem,
    SiteSettings,
)
from apps.home.models import HomePage


class ButtonBlockTests(TestCase):
    def test_external_url_resolves_to_href(self):
        block = ButtonBlock()
        value = block.to_python(
            {"text": "Docs", "external_url": "https://example.com", "style": "primary"}
        )
        self.assertEqual(value.href(), "https://example.com")
        self.assertTrue(value.is_external())
        self.assertEqual(value.display_text(), "Docs")

    def test_internal_page_wins_over_external_url(self):
        home = HomePage.objects.first()
        block = ButtonBlock()
        value = block.to_python(
            {
                "page": home.pk,
                "external_url": "https://example.com",
                "style": "primary",
            }
        )
        self.assertEqual(value.href(), home.url)
        self.assertFalse(value.is_external())

    def test_display_text_falls_back_to_page_title(self):
        home = HomePage.objects.first()
        block = ButtonBlock()
        value = block.to_python({"page": home.pk, "style": "primary"})
        self.assertEqual(value.display_text(), home.title)

    def test_link_without_target_is_invalid(self):
        from wagtail.blocks import StructBlockValidationError

        block = ButtonBlock()
        with self.assertRaises(StructBlockValidationError):
            block.clean(block.to_python({"text": "Nowhere", "style": "primary"}))


class FAQBlockTests(TestCase):
    def test_uid_is_stable_for_same_content(self):
        stream = BodyStreamBlock()
        payload = [
            {
                "type": "faq",
                "value": {
                    "heading": "FAQ",
                    "items": [{"question": "Why?", "answer": "<p>Because.</p>"}],
                },
            }
        ]
        first = stream.to_python(payload)
        second = stream.to_python(payload)
        faq_block = first[0].block
        uid_one = faq_block.get_context(first[0].value)["uid"]
        uid_two = faq_block.get_context(second[0].value)["uid"]
        self.assertEqual(uid_one, uid_two)


class SiteSettingsTests(TestCase):
    def test_social_links_only_include_populated_urls(self):
        site = Site.objects.get(is_default_site=True)
        settings_obj = SiteSettings.objects.create(
            site=site,
            company_name="Endeavours",
            linkedin_url="https://linkedin.com/company/x",
        )
        names = [link["name"] for link in settings_obj.social_links]
        self.assertEqual(names, ["LinkedIn"])

    def test_address_lines_skips_blank_rows(self):
        site = Site.objects.get(is_default_site=True)
        settings_obj = SiteSettings.objects.create(site=site, address="Line one\n\nLine two\n")
        self.assertEqual(settings_obj.address_lines, ["Line one", "Line two"])


class NavigationTests(TestCase):
    def test_menu_item_title_falls_back_to_page_title(self):
        home = HomePage.objects.first()
        menu = NavigationMenu.objects.create(name="Main", slug="main")
        item = NavigationMenuItem.objects.create(menu=menu, page=home, sort_order=0)
        self.assertEqual(item.link_title, home.title)
        self.assertEqual(item.link_url, home.url)
        self.assertFalse(item.is_external)

    def test_external_menu_item(self):
        menu = NavigationMenu.objects.create(name="Main", slug="main")
        item = NavigationMenuItem.objects.create(
            menu=menu, title="Blog", external_url="https://example.com", sort_order=0
        )
        self.assertTrue(item.is_external)
        self.assertEqual(item.link_url, "https://example.com")


class ContextProcessorTests(TestCase):
    def test_main_menu_and_footer_available_in_templates(self):
        home = HomePage.objects.first()
        menu = NavigationMenu.objects.create(name="Main", slug="main")
        NavigationMenuItem.objects.create(
            menu=menu, title="About us", external_url="https://example.com", sort_order=0
        )

        footer = Footer.objects.create(name="Main footer", is_active=True)
        column = FooterColumn.objects.create(footer=footer, heading="Company", sort_order=0)
        FooterLink.objects.create(
            column=column,
            title="Careers",
            external_url="https://example.com/careers",
            sort_order=0,
        )

        response = self.client.get(home.url, HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About us")
        self.assertContains(response, "Careers")
        self.assertEqual(response.context["main_menu"], menu)
        self.assertEqual(response.context["site_footer"], footer)

    def test_site_renders_without_menu_or_footer(self):
        """A fresh install has no snippets configured; it must still render."""
        home = HomePage.objects.first()
        response = self.client.get(home.url, HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
