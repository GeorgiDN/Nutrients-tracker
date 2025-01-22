from django.urls import path
from fitnessApp.food import views

urlpatterns = [
    path('', views.home, name='home'),
    path('meals/<str:username>/', views.user_meals_view, name='user_meals'),
    path('food/new/', views.FoodCreateView.as_view(), name='food-create'),
    path('food/<int:pk>/', views.FoodDetailView.as_view(), name='food-detail'),
    path('food-list/', views.FoodListView.as_view(), name='food-list'),
    path('food/<int:pk>/update/', views.FoodUpdateView.as_view(), name='food-update'),
    path('food/<int:pk>/delete/', views.FoodDeleteView.as_view(), name='food-delete'),
    path('meal/new/', views.MealCreateView.as_view(), name='meal-create'),
    path('meal/<int:pk>/', views.MealDetailView.as_view(), name='meal-detail'),
    path('meal-list/', views.MealListView.as_view(), name='meal-list'),
    path('meal/<int:pk>/update/', views.MealUpdateView.as_view(), name='meal-update'),
    path('meal/<int:pk>/delete/', views.MealDeleteView.as_view(), name='meal-delete'),
    path('mealfood/create/', views.MealFoodCreateView.as_view(), name='mealfood-create'),
    path('mealfood/<int:pk>/', views.MealFoodDetailView.as_view(), name='mealfood-detail'),
    path('mealfood-list/', views.MealFoodListView.as_view(), name='mealfood-list'),
    path('mealfood/<int:pk>/update/', views.MealFoodUpdateView.as_view(), name='mealfood-update'),
    path('mealfood/<int:pk>/delete/', views.MealFoodDeleteView.as_view(), name='mealfood-delete'),
    path('food/navigation/', views.NavigationView.as_view(), name='food-navigation'),
    path('add-common-food/<int:pk>/', views.add_common_food, name='add-common-food'),
    path('common-foods/', views.CommonFoodsListView.as_view(), name='common-foods'),
]
