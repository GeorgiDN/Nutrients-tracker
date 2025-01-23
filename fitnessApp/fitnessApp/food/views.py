from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.urls.base import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin

from fitnessApp.food.forms import MealFoodForm
from fitnessApp.food.models import Food, Meal, MealFood, FoodListTable
from fitnessApp.users.models import UserProfile


def home(request):
    return render(request, 'home/home.html')


@login_required
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
            daily_macronutrients[username][meal.meal_type] = {
                "Meal": meal,
                "Foods": {},
                "Totals": {
                    "Calories": float(meal.total_calories()),
                    "Carbs": float(meal.total_carbs()),
                    "Protein": float(meal.total_protein()),
                    "Fats": float(meal.total_fats()),
                }
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['common_foods'] = FoodListTable.objects.all()
        return context


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


class FoodUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Food
    fields = ['name', 'calories', 'carbs', 'protein', 'fats']
    success_message = "Food was updated!"

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


class MealCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Meal
    fields = ['meal_type', 'order_number']
    success_message = "Meal was created!"

    def form_valid(self, form):
        user_profile = UserProfile.objects.get(user=self.request.user)
        form.instance.user = user_profile
        try:
            meal = form.save()
            return redirect('meal-list')
        except IntegrityError:
            messages.error(self.request, f"You already have a meal with name '{form.instance.meal_type}'")
            return redirect('meal-create')


class MealDetailView(LoginRequiredMixin, DetailView):
    model = Meal

    def get_object(self, queryset=None):
        meal = super().get_object(queryset)
        user_profile = UserProfile.objects.get(user=self.request.user)

        if meal.user != user_profile:
            raise PermissionDenied("You do not have permission to view this meal.")

        return meal


class MealListView(LoginRequiredMixin, ListView):
    model = Food
    template_name = 'food/meal_list.html'
    context_object_name = 'meals'

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user.user_profile)


class MealUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Meal
    fields = ['meal_type', 'order_number']
    success_message = "Meal was updated!"

    def form_valid(self, form):
        form.instance.user = self.request.user.user_profile
        return super().form_valid(form)

    def test_func(self):
        meal = self.get_object()
        return self.request.user == meal.user.user

    def get_success_url(self):
        meal_pk = self.object.pk
        return f"/food/meal-list/#meal-{meal_pk}"


class MealDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Meal
    success_url = reverse_lazy('meal-list')
    success_message = "Meal was successfully deleted."

    def test_func(self):
        meal = self.get_object()
        return self.request.user == meal.user.user


class MealFoodCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = MealFood
    form_class = MealFoodForm
    template_name = 'food/mealfood_form.html'
    success_message = "MealFood was created!"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user.user_profile
        return kwargs

    def get_success_url(self):
        return reverse_lazy('mealfood-list')


class MealFoodDetailView(LoginRequiredMixin, DetailView):
    model = MealFood
    template_name = 'food/mealfood_detail.html'

    def get_object(self, queryset=None):
        meal_food = get_object_or_404(MealFood, pk=self.kwargs['pk'])

        if meal_food.meal.user != self.request.user.user_profile:
            raise PermissionDenied("You do not have permission to view this meal food.")

        return meal_food


class MealFoodListView(LoginRequiredMixin, ListView):
    model = MealFood
    template_name = 'food/mealfood_list.html'
    context_object_name = 'meal_foods'

    def get_queryset(self):
        return MealFood.objects.filter(meal__user=self.request.user.user_profile)


class MealFoodUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = MealFood
    fields = ['meal', 'food', 'grams_quantity']
    success_message = "Meal-Food was updated!"

    def test_func(self):
        meal_food = self.get_object()
        return self.request.user == meal_food.meal.user.user

    def get_success_url(self):
        meal_food_pk = self.object.pk
        return f"/food/mealfood-list/#mealfood-{meal_food_pk}"


class MealFoodDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = MealFood
    success_url = reverse_lazy('mealfood-list')
    success_message = "MealFood was successfully deleted."

    def test_func(self):
        meal_food = self.get_object()
        return self.request.user == meal_food.meal.user.user


@login_required
def add_common_food(request, pk):
    user_profile = UserProfile.objects.get(user=request.user)
    common_food = get_object_or_404(FoodListTable, pk=pk)

    try:
        Food.objects.create(
            user=user_profile,
            name=common_food.name,
            calories=common_food.calories,
            carbs=common_food.carbs,
            protein=common_food.protein,
            fats=common_food.fats
        )
    except IntegrityError:
        messages.error(request, f"You already have a food '{common_food.name}' in your food list.")
    # return redirect(f"{reverse('common-foods')}#food-{pk}")
    return redirect('common-foods')


class CommonFoodsListView(LoginRequiredMixin, ListView):
    model = FoodListTable
    template_name = 'food/common_foods_list.html'
    context_object_name = 'common_foods'

    def get_queryset(self):
        return FoodListTable.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.user_profile
        my_foods = Food.objects.filter(user=user).values_list('name', flat=True)
        context['my_foods'] = my_foods
        return context


class NavigationView(TemplateView):
    template_name = 'food/food-page.html'
