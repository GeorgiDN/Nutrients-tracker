from django.urls import path
from .views import user_meals_view

urlpatterns = [
    path('meals/<str:username>/', user_meals_view, name='user_meals'),
]
