from django.db import models


class FoodMixin(models.Model):
    name = models.CharField(
        max_length=255,
    )
    calories = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )
    carbs = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )
    protein = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )
    fats = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    class Meta:
        abstract = True
