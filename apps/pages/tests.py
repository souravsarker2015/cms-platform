"""Tests for StandardPage."""

from wagtail.test.utils import WagtailPageTestCase

from apps.home.models import HomePage
from apps.pages.models import StandardPage


class StandardPageTests(WagtailPageTestCase):
    def setUp(self):
        self.home = HomePage.objects.first()
        self.page = StandardPage(title="About", slug="about", intro="Who we are.")
        self.home.add_child(instance=self.page)
        self.page.save_revision().publish()

    def test_renders(self):
        response = self.client.get(self.page.url, HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/standard_page.html")
        self.assertContains(response, "Who we are.")

    def test_shows_in_menus_by_default(self):
        """BasePage opts pages into menus so editors don't have to."""
        self.assertTrue(StandardPage.show_in_menus_default)
        fresh = StandardPage(title="Services", slug="services")
        self.home.add_child(instance=fresh)
        self.assertTrue(fresh.show_in_menus)

    def test_can_nest_standard_pages(self):
        self.assertCanCreateAt(StandardPage, StandardPage)

    def test_noindex_flag_renders_meta_tag(self):
        self.page.no_index = True
        self.page.save_revision().publish()
        response = self.client.get(self.page.url, HTTP_HOST="localhost")
        self.assertContains(response, "noindex")
