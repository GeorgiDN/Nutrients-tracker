from django.shortcuts import render
from fitnessApp.users.models import UserProfile


def user_meals_view(request, username):
    user = UserProfile.objects.get(user__username=username)
    daily_macronutrients = {username: {}}

    overall_totals = {
        "Calories": 0,
        "Carbs": 0,
        "Protein": 0,
        "Fats": 0
    }

    all_meals_to_user = user.user_meals.prefetch_related('meal_foods__food')

    for meal in all_meals_to_user:
        if meal.meal_type not in daily_macronutrients[username]:
            daily_macronutrients[username][meal.meal_type] = {}
            daily_macronutrients[username][meal.meal_type]["Foods"] = {}
            daily_macronutrients[username][meal.meal_type]["Totals"] = {
                "Calories": float(meal.total_calories()),
                "Carbs": float(meal.total_carbs()),
                "Protein": float(meal.total_protein()),
                "Fats": float(meal.total_fats()),
            }

            overall_totals["Calories"] += float(meal.total_calories())
            overall_totals["Carbs"] += float(meal.total_carbs())
            overall_totals["Protein"] += float(meal.total_protein())
            overall_totals["Fats"] += float(meal.total_fats())

        for meal_food in meal.meal_foods.all():
            food = meal_food.food
            grams_quantity = meal_food.grams_quantity

            food_key = f'{food.name}'
            quantity_key = f'{grams_quantity}'

            if food_key not in daily_macronutrients[username][meal.meal_type]["Foods"]:
                daily_macronutrients[username][meal.meal_type]["Foods"][food_key] = {}

            daily_macronutrients[username][meal.meal_type]["Foods"][food_key][quantity_key] = {
                'Calories': float((food.calories * grams_quantity) / 100),
                'Carbs': float((food.carbs * grams_quantity) / 100),
                'Protein': float((food.protein * grams_quantity) / 100),
                'Fats': float((food.fats * grams_quantity) / 100)
            }

    daily_macronutrients[username]["Overall Total"] = overall_totals

    context = {
        'daily_macronutrients': daily_macronutrients
    }

    return render(request, 'food/user_meals.html', context)
