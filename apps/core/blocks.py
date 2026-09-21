"""
Reusable StreamField blocks.

Every block here is designed to be dropped into any page's body without
knowing which page it is on. Templates live in
``apps/core/templates/core/blocks/``.
"""

import hashlib

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class LinkValue(blocks.StructValue):
    """Resolves an internal-or-external link down to a single href."""

    def href(self):
        external = self.get("external_url")
        page = self.get("page")
        if page:
            return page.url
        return external or "#"

    def display_text(self):
        text = self.get("text")
        if text:
            return text
        page = self.get("page")
        return page.title if page else ""

    def is_external(self):
        return bool(self.get("external_url") and not self.get("page"))


class LinkBlock(blocks.StructBlock):
    """A link that points at either a Wagtail page or an external URL."""

    text = blocks.CharBlock(
        required=False,
        max_length=80,
        help_text="Leave blank to use the linked page's title.",
    )
    page = blocks.PageChooserBlock(
        required=False,
        help_text="Link to a page on this site.",
    )
    external_url = blocks.URLBlock(
        required=False,
        label="External URL",
        help_text="Used only when no page is chosen.",
    )

    class Meta:
        icon = "link"
        value_class = LinkValue

    def clean(self, value):
        result = super().clean(value)
        if not result.get("page") and not result.get("external_url"):
            raise blocks.StructBlockValidationError(
                non_block_errors=["Choose a page or enter an external URL."]
            )
        return result


class ButtonBlock(LinkBlock):
    """A call-to-action button. Inherits the page/URL link behaviour."""

    style = blocks.ChoiceBlock(
        choices=[
            ("primary", "Primary"),
            ("secondary", "Secondary"),
            ("ghost", "Ghost"),
        ],
        default="primary",
    )

    class Meta:
        icon = "link-external"
        template = "core/blocks/button_block.html"
        label = "Button"
        value_class = LinkValue


class HeroBlock(blocks.StructBlock):
    """Large page-opening banner with an optional background image."""

    eyebrow = blocks.CharBlock(
        required=False,
        max_length=60,
        help_text="Small text above the heading.",
    )
    heading = blocks.CharBlock(max_length=120)
    subheading = blocks.TextBlock(required=False, max_length=300)
    background_image = ImageChooserBlock(required=False)
    alignment = blocks.ChoiceBlock(
        choices=[("left", "Left"), ("center", "Centre")],
        default="left",
    )
    buttons = blocks.ListBlock(ButtonBlock(), max_num=2, required=False)

    class Meta:
        icon = "image"
        template = "core/blocks/hero_block.html"
        label = "Hero"


class RichTextBlock(blocks.RichTextBlock):
    """Prose with a deliberately limited feature set."""

    def __init__(self, **kwargs):
        kwargs.setdefault(
            "features",
            [
                "h2",
                "h3",
                "h4",
                "bold",
                "italic",
                "link",
                "ol",
                "ul",
                "hr",
                "blockquote",
                "document-link",
            ],
        )
        super().__init__(**kwargs)

    class Meta:
        icon = "pilcrow"
        template = "core/blocks/rich_text_block.html"
        label = "Rich text"


class ImageWithCaptionBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False, max_length=250)
    attribution = blocks.CharBlock(required=False, max_length=120)
    width = blocks.ChoiceBlock(
        choices=[
            ("standard", "Standard"),
            ("wide", "Wide"),
            ("full", "Full bleed"),
        ],
        default="standard",
    )

    class Meta:
        icon = "image"
        template = "core/blocks/image_with_caption_block.html"
        label = "Image"


class FeatureCardBlock(blocks.StructBlock):
    """One card inside a FeatureGrid."""

    icon = blocks.ChoiceBlock(
        choices=[
            ("bolt", "Bolt"),
            ("shield", "Shield"),
            ("chart", "Chart"),
            ("gear", "Gear"),
            ("globe", "Globe"),
            ("users", "Users"),
            ("sparkle", "Sparkle"),
            ("check", "Check"),
        ],
        default="bolt",
        help_text="Chosen from a fixed icon set so cards stay consistent.",
    )
    title = blocks.CharBlock(max_length=80)
    text = blocks.TextBlock(max_length=300)
    link = LinkBlock(required=False)

    class Meta:
        icon = "form"
        label = "Feature card"


class FeatureGridBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, max_length=120)
    intro = blocks.TextBlock(required=False, max_length=300)
    columns = blocks.ChoiceBlock(
        choices=[("2", "Two"), ("3", "Three"), ("4", "Four")],
        default="3",
    )
    cards = blocks.ListBlock(FeatureCardBlock(), min_num=1)

    class Meta:
        icon = "grip"
        template = "core/blocks/feature_grid_block.html"
        label = "Feature grid"


class CallToActionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=120)
    text = blocks.TextBlock(required=False, max_length=300)
    buttons = blocks.ListBlock(ButtonBlock(), min_num=1, max_num=2)
    style = blocks.ChoiceBlock(
        choices=[
            ("accent", "Accent background"),
            ("muted", "Muted background"),
        ],
        default="accent",
    )

    class Meta:
        icon = "megaphone"
        template = "core/blocks/call_to_action_block.html"
        label = "Call to action"


class TestimonialBlock(blocks.StructBlock):
    quote = blocks.TextBlock(max_length=500)
    author_name = blocks.CharBlock(max_length=80)
    author_role = blocks.CharBlock(required=False, max_length=120)
    author_image = ImageChooserBlock(required=False)
    company_logo = ImageChooserBlock(required=False)

    class Meta:
        icon = "openquote"
        template = "core/blocks/testimonial_block.html"
        label = "Testimonial"


class StatBlock(blocks.StructBlock):
    value = blocks.CharBlock(
        max_length=20,
        help_text="For example: 98%, 1.2M, 24/7",
    )
    label = blocks.CharBlock(max_length=80)

    class Meta:
        icon = "table"
        label = "Statistic"


class StatsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, max_length=120)
    stats = blocks.ListBlock(StatBlock(), min_num=1, max_num=4)

    class Meta:
        icon = "table"
        template = "core/blocks/stats_block.html"
        label = "Stats"


class FAQItemBlock(blocks.StructBlock):
    question = blocks.CharBlock(max_length=200)
    answer = blocks.RichTextBlock(features=["bold", "italic", "link", "ol", "ul"])

    class Meta:
        icon = "help"
        label = "Question"


class FAQBlock(blocks.StructBlock):
    """Accordion. Expand/collapse behaviour is handled by Alpine.js."""

    heading = blocks.CharBlock(required=False, max_length=120)
    items = blocks.ListBlock(FAQItemBlock(), min_num=1)

    class Meta:
        icon = "help"
        template = "core/blocks/faq_block.html"
        label = "FAQ"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        # Element ids must be unique within the document and stable between
        # requests, so anchors and cached HTML stay valid. Derive them from the
        # question text rather than object identity.
        questions = "|".join(str(item.get("question", "")) for item in value.get("items", []))
        context["uid"] = hashlib.md5(questions.encode(), usedforsecurity=False).hexdigest()[:8]
        return context


class BodyStreamBlock(blocks.StreamBlock):
    """The standard set of blocks available in a page body."""

    hero = HeroBlock()
    rich_text = RichTextBlock()
    image = ImageWithCaptionBlock()
    feature_grid = FeatureGridBlock()
    call_to_action = CallToActionBlock()
    testimonial = TestimonialBlock()
    stats = StatsBlock()
    faq = FAQBlock()

    class Meta:
        block_counts = {"hero": {"max_num": 1}}
