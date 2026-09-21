"""
Shared models: the custom image model, the abstract SEO-aware base page,
and the editable snippets/settings that drive site chrome.
"""

from django.db import models
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet


class CustomImage(AbstractImage):
    """
    Project image model. Defined up front because swapping the image model
    after content exists is painful.
    """

    caption = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional default caption.",
    )

    admin_form_fields = (*Image.admin_form_fields, "caption")


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage,
        on_delete=models.CASCADE,
        related_name="renditions",
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


class BasePage(Page):
    """
    Abstract page with the SEO fields every page on the site should carry.

    Wagtail's own ``seo_title`` and ``search_description`` are reused where they
    fit; the extras here cover Open Graph and indexing control.
    """

    og_image = models.ForeignKey(
        "core.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Social share image",
        help_text="Shown when this page is shared on social media. 1200x630 works best.",
    )
    og_title = models.CharField(
        max_length=95,
        blank=True,
        verbose_name="Social share title",
        help_text="Defaults to the page's SEO title, then the page title.",
    )
    og_description = models.TextField(
        max_length=200,
        blank=True,
        verbose_name="Social share description",
        help_text="Defaults to the meta description.",
    )
    no_index = models.BooleanField(
        default=False,
        verbose_name="Hide from search engines",
        help_text="Adds a noindex tag. Use for thank-you or landing pages.",
    )

    # Most pages on a corporate site belong in the navigation.
    show_in_menus_default = True

    promote_panels = [
        MultiFieldPanel(
            [
                FieldPanel("slug"),
                FieldPanel("seo_title"),
                FieldPanel("search_description"),
                FieldPanel("show_in_menus"),
            ],
            heading="Page metadata",
        ),
        MultiFieldPanel(
            [
                FieldPanel("og_title"),
                FieldPanel("og_description"),
                FieldPanel("og_image"),
            ],
            heading="Social sharing",
        ),
        MultiFieldPanel(
            [FieldPanel("no_index")],
            heading="Search engine visibility",
        ),
    ]

    search_fields = [*Page.search_fields]

    class Meta:
        abstract = True

    # -- Template helpers -------------------------------------------------

    @cached_property
    def meta_title(self):
        return self.seo_title or self.title

    @cached_property
    def meta_description(self):
        return self.search_description

    @cached_property
    def social_title(self):
        return self.og_title or self.seo_title or self.title

    @cached_property
    def social_description(self):
        return self.og_description or self.search_description

    @cached_property
    def social_image(self):
        return self.og_image


# ---------------------------------------------------------------------------
# Site settings
# ---------------------------------------------------------------------------


@register_setting(icon="cog")
class SiteSettings(BaseSiteSetting):
    """Company details reused across the site chrome."""

    company_name = models.CharField(max_length=120, default="Endeavours")
    tagline = models.CharField(max_length=200, blank=True)
    logo = models.ForeignKey(
        "core.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    logo_dark = models.ForeignKey(
        "core.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Optional alternate logo for dark backgrounds, such as the footer.",
    )
    favicon = models.ForeignKey(
        "core.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=40, blank=True)
    address = models.TextField(blank=True, help_text="One line per row.")

    twitter_url = models.URLField(blank=True, verbose_name="X / Twitter URL")
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn URL")
    facebook_url = models.URLField(blank=True, verbose_name="Facebook URL")
    instagram_url = models.URLField(blank=True, verbose_name="Instagram URL")
    youtube_url = models.URLField(blank=True, verbose_name="YouTube URL")
    github_url = models.URLField(blank=True, verbose_name="GitHub URL")

    default_og_image = models.ForeignKey(
        "core.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Fallback social share image for pages without their own.",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("company_name"),
                FieldPanel("tagline"),
                FieldPanel("logo"),
                FieldPanel("logo_dark"),
                FieldPanel("favicon"),
            ],
            heading="Brand",
        ),
        MultiFieldPanel(
            [
                FieldPanel("contact_email"),
                FieldPanel("contact_phone"),
                FieldPanel("address"),
            ],
            heading="Contact",
        ),
        MultiFieldPanel(
            [
                FieldPanel("twitter_url"),
                FieldPanel("linkedin_url"),
                FieldPanel("facebook_url"),
                FieldPanel("instagram_url"),
                FieldPanel("youtube_url"),
                FieldPanel("github_url"),
            ],
            heading="Social links",
        ),
        MultiFieldPanel(
            [FieldPanel("default_og_image")],
            heading="Defaults",
        ),
    ]

    class Meta:
        verbose_name = "Site settings"

    @cached_property
    def social_links(self):
        """The populated social links, ready to iterate in a template."""
        candidates = [
            ("X", self.twitter_url, "twitter"),
            ("LinkedIn", self.linkedin_url, "linkedin"),
            ("Facebook", self.facebook_url, "facebook"),
            ("Instagram", self.instagram_url, "instagram"),
            ("YouTube", self.youtube_url, "youtube"),
            ("GitHub", self.github_url, "github"),
        ]
        return [{"name": name, "url": url, "icon": icon} for name, url, icon in candidates if url]

    @cached_property
    def address_lines(self):
        return [line for line in self.address.splitlines() if line.strip()]


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------


class MenuItemMixin(models.Model):
    """Link fields shared by top-level menu items and their children."""

    title = models.CharField(
        max_length=80,
        blank=True,
        help_text="Leave blank to use the linked page's title.",
    )
    page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
    )
    external_url = models.URLField(blank=True, verbose_name="External URL")

    class Meta:
        abstract = True

    def __str__(self):
        return self.link_title

    @property
    def link_title(self):
        if self.title:
            return self.title
        if self.page:
            return self.page.title
        return self.external_url

    @property
    def link_url(self):
        if self.page:
            return self.page.url
        return self.external_url

    @property
    def is_external(self):
        return bool(self.external_url and not self.page)


@register_snippet
class NavigationMenu(ClusterableModel):
    """
    A named, ordered, two-level menu. Editors manage these from
    Snippets -> Navigation menus.
    """

    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(
        max_length=80,
        unique=True,
        help_text="Used to pull this menu into a template, e.g. 'main'.",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        InlinePanel("items", label="Menu item"),
    ]

    class Meta:
        verbose_name = "Navigation menu"
        ordering = ["name"]

    def __str__(self):
        return self.name


class NavigationMenuItem(Orderable, ClusterableModel, MenuItemMixin):
    menu = ParentalKey(
        NavigationMenu,
        on_delete=models.CASCADE,
        related_name="items",
    )
    highlight = models.BooleanField(
        default=False,
        help_text="Render this item as a button. Use for one call to action.",
    )

    panels = [
        FieldPanel("title"),
        PageChooserPanel("page"),
        FieldPanel("external_url"),
        FieldPanel("highlight"),
        InlinePanel("children", label="Sub-item"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "Menu item"


class NavigationMenuChildItem(Orderable, MenuItemMixin):
    """Second-level item, rendered inside a dropdown."""

    parent = ParentalKey(
        NavigationMenuItem,
        on_delete=models.CASCADE,
        related_name="children",
    )
    description = models.CharField(
        max_length=120,
        blank=True,
        help_text="Optional supporting line shown under the link.",
    )

    panels = [
        FieldPanel("title"),
        PageChooserPanel("page"),
        FieldPanel("external_url"),
        FieldPanel("description"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "Sub-item"


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------


@register_snippet
class Footer(ClusterableModel):
    """Footer content: intro blurb, link columns, and legal line."""

    name = models.CharField(
        max_length=80,
        default="Main footer",
        help_text="Internal name only.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="The most recently created active footer is the one rendered.",
    )
    intro = RichTextField(
        blank=True,
        features=["bold", "italic", "link"],
        help_text="Short blurb shown beside the link columns.",
    )
    copyright_text = models.CharField(
        max_length=200,
        blank=True,
        help_text="Shown after the year. Example: Endeavours Ltd. All rights reserved.",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("is_active"),
        FieldPanel("intro"),
        InlinePanel("columns", label="Column"),
        FieldPanel("copyright_text"),
        InlinePanel("legal_links", label="Legal link"),
    ]

    class Meta:
        verbose_name = "Footer"
        ordering = ["name"]

    def __str__(self):
        return self.name


class FooterColumn(Orderable, ClusterableModel):
    footer = ParentalKey(Footer, on_delete=models.CASCADE, related_name="columns")
    heading = models.CharField(max_length=60)

    panels = [
        FieldPanel("heading"),
        InlinePanel("links", label="Link"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "Footer column"

    def __str__(self):
        return self.heading


class FooterLink(Orderable, MenuItemMixin):
    column = ParentalKey(FooterColumn, on_delete=models.CASCADE, related_name="links")

    panels = [
        FieldPanel("title"),
        PageChooserPanel("page"),
        FieldPanel("external_url"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "Footer link"


class FooterLegalLink(Orderable, MenuItemMixin):
    """Small links in the footer's bottom bar, e.g. Privacy, Terms."""

    footer = ParentalKey(Footer, on_delete=models.CASCADE, related_name="legal_links")

    panels = [
        FieldPanel("title"),
        PageChooserPanel("page"),
        FieldPanel("external_url"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "Legal link"
