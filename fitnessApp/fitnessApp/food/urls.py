from django.urls import path
from fitnessApp.food import views

urlpatterns = [
    path('', views.home, name='home'),
    path('meals/<str:username>/', views.user_meals_view, name='user_meals'),
    path('food/new/', views.FoodCreateView.as_view(), name='food-create'),
    path('food/<int:pk>/', views.FoodDetailView.as_view(), name='food-detail'),
    path('food-list/', views.FoodListView.as_view(), name='food-list'),
    path('food/<int:pk>/update/', views.FoodUpdateView.as_view(), name='food-update'),
]
