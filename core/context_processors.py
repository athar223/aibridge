from django.conf import settings


def site_meta(request):
    """Expose site-wide branding constants to every template."""
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "AIBridge"),
        "SITE_TAGLINE": getattr(settings, "SITE_TAGLINE", "Bridging People with AI"),
    }
