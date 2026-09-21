"""Generic content pages: About, Services, and similar."""

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images import get_image_model_string
from wagtail.search import index

from apps.core.blocks import BodyStreamBlock
from apps.core.models import BasePage


class StandardPage(BasePage):
    """A flexible content page driven by the shared block library."""

    intro = models.TextField(
        max_length=500,
        blank=True,
        help_text="Short summary shown under the page title.",
    )
    header_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Optional banner image behind the page title.",
    )
    body = StreamField(
        BodyStreamBlock(),
        blank=True,
    )

    content_panels = [
        *BasePage.content_panels,
        FieldPanel("intro"),
        FieldPanel("header_image"),
        FieldPanel("body"),
    ]

    search_fields = [
        *BasePage.search_fields,
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    parent_page_types = ["home.HomePage", "pages.StandardPage"]
    subpage_types = ["pages.StandardPage"]

    class Meta:
        verbose_name = "Standard page"
