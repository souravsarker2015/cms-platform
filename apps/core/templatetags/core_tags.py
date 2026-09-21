"""Template helpers shared across the site."""

from django import template
from django.utils import timezone

from ..models import NavigationMenu

register = template.Library()


@register.simple_tag
def current_year():
    return timezone.now().year


@register.simple_tag(takes_context=True)
def get_menu(context, slug):
    """Fetch a navigation menu by slug, for menus other than the main one."""
    return (
        NavigationMenu.objects.filter(slug=slug)
        .prefetch_related("items__page", "items__children__page")
        .first()
    )


@register.simple_tag(takes_context=True)
def is_active_page(context, page):
    """
    True when ``page`` is the page being viewed or one of its ancestors, so
    navigation can mark the current section.
    """
    if page is None:
        return False
    current = context.get("page")
    if current is None:
        request = context.get("request")
        current = getattr(request, "_wagtail_route_for_request", None)
    if current is None:
        return False
    if current.pk == page.pk:
        return True
    return current.get_ancestors().filter(pk=page.pk).exists()


@register.filter
def menu_url(item):
    """Resolve a menu item or footer link to its href."""
    return item.link_url or "#"
