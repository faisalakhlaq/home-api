from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeTracking(models.Model):
    """
    An abstract base model that provides self-updating timestamp fields for
    creation and modification tracking.

    This model adds two automatically managed fields:
    - created_at: DateTime set to the current timestamp when a record is first
        created
    - updated_at: DateTime updated to the current timestamp whenever the record
        is saved

    Intended to be inherited by other models to provide consistent timestamp
    tracking without having to redefine these common fields. The model is
    abstract and won't create its own database table.

    Features:
    - Auto-created/updated timestamps
    - Internationalization-ready field labels and help texts
    - Suitable for use as a mixin in any model requiring time tracking
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Creation Date & Time"),
        help_text=_("The date and time when this record was first created."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Update Date & Time"),
        help_text=_("The date and time when this record was last updated."),
    )

    class Meta:
        abstract = True
        verbose_name = _("Time Tracking")
        verbose_name_plural = _("Time Tracking")
