from django.utils.translation import gettext_lazy


def _(*args, **kwargs):
    """
    Core wrapper for wrapping strings for translation.

    This function is mostly added for easy importing, avoiding the need to use:
    from django.utils.translation import gettext_lazy as _
    """
    return gettext_lazy(*args, **kwargs)
