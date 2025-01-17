from django.contrib import admin

from fitnessApp.food.models import Food, Meal, MealFood


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'carbs', 'protein', 'fats')


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_type', )


@admin.register(MealFood)
class MealFoodAdmin(admin.ModelAdmin):
    list_display = ('meal', 'food', 'grams_quantity' )
