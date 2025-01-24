from django.db import models

from django.contrib.auth.models import User

from fitnessApp.food.models_mixins import NutritionMixin


class UserProfile(NutritionMixin, models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user_profile"
    )

    def __str__(self):
        return self.user.username
