"""
Populate a fresh install with representative content.

Useful for local development and for showing editors what each block looks
like. Safe to re-run: it updates the existing objects rather than duplicating.
"""

import json
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.models import Site

from apps.core.models import (
    Footer,
    FooterColumn,
    FooterLegalLink,
    FooterLink,
    NavigationMenu,
    NavigationMenuChildItem,
    NavigationMenuItem,
    SiteSettings,
)
from apps.home.models import HomePage
from apps.pages.models import StandardPage


class Command(BaseCommand):
    help = "Create the admin user plus demo navigation, footer, settings and pages. Safe to re-run."

    def add_arguments(self, parser):
        parser.add_argument(
            "--admin-username",
            default=os.environ.get("SEED_ADMIN_USERNAME", "admin"),
            help="Admin username to create (default: admin).",
        )
        parser.add_argument(
            "--admin-email",
            default=os.environ.get("SEED_ADMIN_EMAIL", "admin@endeavours.example"),
            help="Admin email address.",
        )
        parser.add_argument(
            "--admin-password",
            default=os.environ.get("SEED_ADMIN_PASSWORD", "admin123456"),
            help="Admin password. Development convenience only - change it "
            "anywhere the site is reachable by others.",
        )
        parser.add_argument(
            "--skip-admin",
            action="store_true",
            help="Do not create or update the admin user.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        site = Site.objects.get(is_default_site=True)
        home = HomePage.objects.first()
        if home is None:
            self.stderr.write("No HomePage found. Run migrate first.")
            return

        if not options["skip_admin"]:
            self._admin_user(options)

        self._site_settings(site)
        pages = self._pages(home)
        self._homepage(home)
        self._navigation(home, pages)
        self._footer(home, pages)

        self.stdout.write(self.style.SUCCESS("Demo content created."))

    # -- Admin user -------------------------------------------------------

    def _admin_user(self, options):
        User = get_user_model()
        username = options["admin_username"]
        password = options["admin_password"]

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": options["admin_email"],
                "is_staff": True,
                "is_superuser": True,
            },
        )
        # Always reset the flags and password so a half-made account still
        # ends up usable.
        user.email = options["admin_email"]
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        verb = "Created" if created else "Updated"
        self.stdout.write(f"{verb} superuser '{username}'.")
        self.stdout.write(
            self.style.WARNING(
                "  Development credentials. Change this password before the "
                "site is reachable by anyone else."
            )
        )

    # -- Settings ---------------------------------------------------------

    def _site_settings(self, site):
        settings_obj, _ = SiteSettings.objects.get_or_create(site=site)
        settings_obj.company_name = "Endeavours"
        settings_obj.tagline = "Digital engineering for companies that ship."
        settings_obj.contact_email = "hello@endeavours.example"
        settings_obj.contact_phone = "+880 1700 000000"
        settings_obj.address = "Level 8, Tech Tower\nGulshan Avenue\nDhaka 1212"
        settings_obj.linkedin_url = "https://www.linkedin.com/company/example"
        settings_obj.twitter_url = "https://x.com/example"
        settings_obj.github_url = "https://github.com/example"
        settings_obj.save()

    # -- Pages ------------------------------------------------------------

    def _pages(self, home):
        specs = [
            (
                "About",
                "about",
                "Who we are and how we work.",
                "We are a team of engineers, designers and strategists building "
                "software that holds up under real load.",
            ),
            (
                "Services",
                "services",
                "What we do.",
                "From discovery through to run-and-maintain, we cover the full delivery lifecycle.",
            ),
            (
                "Contact",
                "contact",
                "Start a conversation.",
                "Tell us what you are building and we will come back within one working day.",
            ),
        ]
        created = {}
        for title, slug, intro, body_text in specs:
            page = StandardPage.objects.filter(slug=slug).first()
            if page is None:
                page = StandardPage(title=title, slug=slug)
                home.add_child(instance=page)
            page.intro = intro
            page.body = json.dumps(
                [
                    {
                        "type": "rich_text",
                        "value": f"<h2>{title}</h2><p>{body_text}</p>",
                    }
                ]
            )
            page.save_revision().publish()
            created[slug] = page
        return created

    # -- Homepage ---------------------------------------------------------

    def _homepage(self, home):
        home.hero_eyebrow = "Engineering partners"
        home.hero_heading = "Build what moves your business forward"
        home.hero_subheading = (
            "Endeavours designs, builds and runs the digital systems that "
            "serious companies depend on."
        )
        home.hero_buttons = json.dumps(
            [
                {
                    "type": "button",
                    "value": {
                        "text": "Start a project",
                        "page": None,
                        "external_url": "https://example.com/contact",
                        "style": "primary",
                    },
                },
                {
                    "type": "button",
                    "value": {
                        "text": "See our work",
                        "page": None,
                        "external_url": "https://example.com/work",
                        "style": "secondary",
                    },
                },
            ]
        )
        home.body = json.dumps(
            [
                {
                    "type": "feature_grid",
                    "value": {
                        "heading": "What we do",
                        "intro": "Four disciplines, one delivery team.",
                        "columns": "3",
                        "cards": [
                            {
                                "icon": "bolt",
                                "title": "Product engineering",
                                "text": "Web platforms and APIs built to scale with your business.",
                                "link": {},
                            },
                            {
                                "icon": "shield",
                                "title": "Security and compliance",
                                "text": "Hardened systems, audited pipelines, and sensible defaults.",
                                "link": {},
                            },
                            {
                                "icon": "chart",
                                "title": "Data and analytics",
                                "text": "Turn operational data into decisions leaders can act on.",
                                "link": {},
                            },
                        ],
                    },
                },
                {
                    "type": "stats",
                    "value": {
                        "heading": "Measured by outcomes",
                        "stats": [
                            {"value": "120+", "label": "Projects delivered"},
                            {"value": "99.9%", "label": "Uptime across managed services"},
                            {"value": "14", "label": "Countries served"},
                            {"value": "24/7", "label": "Support coverage"},
                        ],
                    },
                },
                {
                    "type": "testimonial",
                    "value": {
                        "quote": (
                            "They took a tangled legacy system and turned it into "
                            "something our team can actually build on."
                        ),
                        "author_name": "Farhana Rahman",
                        "author_role": "CTO, Meridian Logistics",
                        "author_image": None,
                        "company_logo": None,
                    },
                },
                {
                    "type": "faq",
                    "value": {
                        "heading": "Frequently asked questions",
                        "items": [
                            {
                                "question": "How do engagements usually start?",
                                "answer": "<p>Most begin with a short paid discovery so we can scope accurately before committing to a build.</p>",
                            },
                            {
                                "question": "Do you work with existing teams?",
                                "answer": "<p>Yes. We regularly embed alongside in-house engineers and hand over fully documented work.</p>",
                            },
                            {
                                "question": "What happens after launch?",
                                "answer": "<p>We offer ongoing support and managed hosting, or a clean handover if you prefer to run it yourself.</p>",
                            },
                        ],
                    },
                },
            ]
        )
        home.cta_heading = "Let's talk about what you're building"
        home.cta_text = "Tell us the problem. We'll tell you how we'd approach it."
        home.cta_buttons = json.dumps(
            [
                {
                    "type": "button",
                    "value": {
                        "text": "Get in touch",
                        "page": None,
                        "external_url": "https://example.com/contact",
                        "style": "primary",
                    },
                }
            ]
        )
        home.search_description = (
            "Endeavours designs, builds and runs digital systems for companies that depend on them."
        )
        home.save_revision().publish()

    # -- Navigation -------------------------------------------------------

    def _navigation(self, home, pages):
        menu, _ = NavigationMenu.objects.get_or_create(slug="main", defaults={"name": "Main menu"})
        menu.items.all().delete()

        about = NavigationMenuItem.objects.create(menu=menu, page=pages["about"], sort_order=0)
        NavigationMenuChildItem.objects.create(
            parent=about,
            title="Our story",
            page=pages["about"],
            description="How Endeavours started.",
            sort_order=0,
        )
        NavigationMenuChildItem.objects.create(
            parent=about,
            title="Careers",
            external_url="https://example.com/careers",
            description="Open roles across engineering and design.",
            sort_order=1,
        )

        NavigationMenuItem.objects.create(menu=menu, page=pages["services"], sort_order=1)
        NavigationMenuItem.objects.create(
            menu=menu, page=pages["contact"], highlight=True, sort_order=2
        )

    # -- Footer -----------------------------------------------------------

    def _footer(self, home, pages):
        footer, _ = Footer.objects.get_or_create(name="Main footer")
        footer.is_active = True
        footer.intro = (
            "<p>Endeavours is a digital engineering studio working with "
            "ambitious teams across logistics, fintech and health.</p>"
        )
        footer.copyright_text = "Endeavours Ltd. All rights reserved."
        footer.save()

        footer.columns.all().delete()
        footer.legal_links.all().delete()

        company = FooterColumn.objects.create(footer=footer, heading="Company", sort_order=0)
        FooterLink.objects.create(column=company, page=pages["about"], sort_order=0)
        FooterLink.objects.create(column=company, page=pages["contact"], sort_order=1)

        services = FooterColumn.objects.create(footer=footer, heading="Services", sort_order=1)
        FooterLink.objects.create(column=services, page=pages["services"], sort_order=0)
        FooterLink.objects.create(
            column=services,
            title="Support",
            external_url="https://example.com/support",
            sort_order=1,
        )

        FooterLegalLink.objects.create(
            footer=footer,
            title="Privacy",
            external_url="https://example.com/privacy",
            sort_order=0,
        )
        FooterLegalLink.objects.create(
            footer=footer,
            title="Terms",
            external_url="https://example.com/terms",
            sort_order=1,
        )
