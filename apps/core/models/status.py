from django.db import models
from django.contrib.contenttypes.models import ContentType


class Status(models.Model):
    name = models.CharField(max_length=255, help_text="Title or name of the status.")
    description = models.CharField(
        max_length=255,
        blank=True,
        help_text="A short description of the type | genre. max 255 characters.",
    )
    model = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        help_text="The model on which this status will be used.",
    )
    sorting_order = models.IntegerField(
        default=1,
        help_text="""User defined sorting to control order in the dropdown.
        Number for status among multiple status.""",
    )
    active = models.BooleanField(
        default=True,
        help_text="If set false then it should not appear in the status list.",
    )

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "model"], name="unique_model_status_name"
            ),
        ]

    def __str__(self) -> str:
        return self.name
