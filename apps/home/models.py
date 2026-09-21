"""The site's homepage."""

from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.images import get_image_model_string
from wagtail.search import index

from apps.core.blocks import BodyStreamBlock, ButtonBlock
from apps.core.models import BasePage


class HomePage(BasePage):
    """
    The site root. The hero is modelled as dedicated fields rather than a
    StreamField block so it is always present and always first.
    """

    # -- Hero -------------------------------------------------------------
    hero_eyebrow = models.CharField(
        max_length=60,
        blank=True,
        help_text="Small line above the headline.",
    )
    hero_heading = models.CharField(
        max_length=120,
        blank=True,
        help_text="The main headline. Defaults to the page title if blank.",
    )
    hero_subheading = models.TextField(
        max_length=300,
        blank=True,
    )
    hero_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    hero_buttons = StreamField(
        [("button", ButtonBlock())],
        blank=True,
        max_num=2,
        help_text="Up to two buttons in the hero.",
    )

    # -- Body -------------------------------------------------------------
    body = StreamField(
        BodyStreamBlock(),
        blank=True,
        help_text="Build the page from the available sections.",
    )

    # -- Closing call to action -------------------------------------------
    cta_heading = models.CharField(max_length=120, blank=True)
    cta_text = models.TextField(max_length=300, blank=True)
    cta_buttons = StreamField(
        [("button", ButtonBlock())],
        blank=True,
        max_num=2,
    )

    content_panels = [
        *BasePage.content_panels,
        MultiFieldPanel(
            [
                FieldPanel("hero_eyebrow"),
                FieldPanel("hero_heading"),
                FieldPanel("hero_subheading"),
                FieldPanel("hero_image"),
                FieldPanel("hero_buttons"),
            ],
            heading="Hero",
        ),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("cta_heading"),
                FieldPanel("cta_text"),
                FieldPanel("cta_buttons"),
            ],
            heading="Closing call to action",
        ),
    ]

    search_fields = [
        *BasePage.search_fields,
        index.SearchField("hero_heading"),
        index.SearchField("hero_subheading"),
        index.SearchField("body"),
    ]

    # Only one homepage, and it lives at the site root.
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["pages.StandardPage"]

    class Meta:
        verbose_name = "Home page"

    @property
    def heading(self):
        return self.hero_heading or self.title

    @property
    def has_cta(self):
        return bool(self.cta_heading)
