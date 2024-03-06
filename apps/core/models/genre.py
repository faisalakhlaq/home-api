from django.contrib.contenttypes.models import ContentType
from django.db import models


class Genre(models.Model):
    """`Genre` represents a generic type for an object.

    Create a new genre | type and assign it to a model object.

    Attributes:
        name (str): Name for the genre.
        description (str): A short description of what the genre is.
        sorting_order (int): To control order in the dropdown. This is the user defined sorting.
        active (bool): If set false then it should not appear in the types.
        This helps to control what should appear in the types while not deleting any existing one.
    """

    name = models.CharField(max_length=255, help_text="Name for the type | genre.")
    description = models.CharField(
        max_length=255,
        blank=True,
        help_text="A short description of the type | genre. max 255 characters.",
    )
    sorting_order = models.IntegerField(
        blank=True,
        null=True,
        help_text="To control order in the dropdown. This is the user defined sorting.",
    )
    active = models.BooleanField(
        default=True,
        help_text="Set to false to indicate that it will no longer be utilized.",
    )
    model = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        help_text="Model on which this genre will be used.",
    )

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "model"], name="unique_model_genre_name"
            ),
        ]
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.name
