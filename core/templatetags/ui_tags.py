from django import template

register = template.Library()


@register.inclusion_tag("core/partials/ui_button.html")
def button(label, url, variant="primary"):
    """
    Renders the shared Button component.

    variant: "primary" | "secondary" | "tertiary" — matches the three button
    styles defined in the design system (Section 4 of the build spec).
    """
    return {"label": label, "url": url, "variant": variant}


@register.filter
def get_item(dictionary, key):
    """Look up a dict value by a variable key — Django templates can't do
    `mega_menus[item.megamenu]` directly, so the mega-menu loop uses this."""
    if not key or not dictionary:
        return []
    return dictionary.get(key, [])
