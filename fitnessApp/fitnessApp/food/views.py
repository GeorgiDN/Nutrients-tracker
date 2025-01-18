from django.db import IntegrityError
from django.urls.base import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from fitnessApp.food.models import Food
from fitnessApp.users.models import UserProfile


def home(request):
    return render(request, 'home/home.html')


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

            if food not in daily_macronutrients[username][meal.meal_type]["Foods"]:
                daily_macronutrients[username][meal.meal_type]["Foods"][food] = {}

            daily_macronutrients[username][meal.meal_type]["Foods"][food][grams_quantity] = {
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


class FoodCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Food
    fields = ['name', 'calories', 'carbs', 'protein', 'fats']
    success_message = "Food was created!"

    def form_valid(self, form):
        user_profile = UserProfile.objects.get(user=self.request.user)
        form.instance.user = user_profile
        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, f"You already have a food '{form.instance.name}' added to food list.")
            return redirect('food-create')


class FoodDetailView(LoginRequiredMixin, DetailView):
    model = Food

    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        return Food.objects.filter(user=user_profile)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user_profile = UserProfile.objects.get(user=self.request.user)
        if obj.user != user_profile:
            raise PermissionDenied("You do not have permission to view this food.")
        return obj


class FoodListView(LoginRequiredMixin, ListView):
    model = Food
    template_name = 'food/food_list.html'
    context_object_name = 'foods'

    def get_queryset(self):
        return Food.objects.filter(user=self.request.user.user_profile)


class FoodUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Food
    fields = ['name', 'calories', 'carbs', 'protein', 'fats']

    def form_valid(self, form):
        form.instance.user = self.request.user.user_profile
        return super().form_valid(form)

    def test_func(self):
        food = self.get_object()
        return self.request.user == food.user.user

    def get_success_url(self):
        food_pk = self.object.pk
        return f"/food/food-list/#food-{food_pk}"


class FoodDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Food
    success_url = reverse_lazy('food-list')
    success_message = "Food was successfully deleted."

    def test_func(self):
        food = self.get_object()
        return self.request.user == food.user.user
