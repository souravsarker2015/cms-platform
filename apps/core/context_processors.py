"""Makes site chrome available to every template without per-view plumbing."""

from .models import Footer, NavigationMenu

MAIN_MENU_SLUG = "main"


def navigation(request):
    """
    Adds the main navigation menu and the active footer to the context.

    Both are optional: a fresh site with no snippets configured still renders.
    """
    menu = (
        NavigationMenu.objects.filter(slug=MAIN_MENU_SLUG)
        .prefetch_related("items__page", "items__children__page")
        .first()
    )
    footer = (
        Footer.objects.filter(is_active=True)
        .prefetch_related("columns__links__page", "legal_links__page")
        .order_by("-pk")
        .first()
    )
    return {
        "main_menu": menu,
        "site_footer": footer,
    }
