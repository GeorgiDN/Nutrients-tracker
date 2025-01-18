from django.db import models
from fitnessApp.users.models import UserProfile
from django.urls.base import reverse


class Food(models.Model):
    user = models.ForeignKey(
        to=UserProfile,
        on_delete=models.CASCADE,
        related_name='user_foods',
        blank=True,
        null=True,
    )
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

    def get_absolute_url(self):
        return reverse('food-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'user')


class Meal(models.Model):
    user = models.ForeignKey(
        to=UserProfile,
        on_delete=models.CASCADE,
        related_name='user_meals',
    )
    meal_type = models.CharField(
        max_length=30,
    )
    food = models.ManyToManyField(
        to=Food,
        through='MealFood',
        related_name='meals',
    )

    class Meta:
        unique_together = ('meal_type', 'user')

    def __str__(self):
        return f'{self.user.user.username} - {self.meal_type}'

    def total_calories(self):
        total = sum((item.food.calories * item.grams_quantity) / 100 for item in self.meal_foods.all())
        return total

    def total_carbs(self):
        total = sum((item.food.carbs * item.grams_quantity) / 100 for item in self.meal_foods.all())
        return total

    def total_fats(self):
        total = sum((item.food.fats * item.grams_quantity) / 100 for item in self.meal_foods.all())
        return total

    def total_protein(self):
        total = sum((item.food.protein * item.grams_quantity) / 100 for item in self.meal_foods.all())
        return total


class MealFood(models.Model):
    meal = models.ForeignKey(
        to=Meal,
        on_delete=models.CASCADE,
        related_name='meal_foods'
    )
    food = models.ForeignKey(
        to=Food,
        on_delete=models.CASCADE,
    )
    grams_quantity = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f'{self.meal} - {self.food.name} ({self.grams_quantity}g)'

    class Meta:
        unique_together = ('meal', 'food')
