from django import forms
from .models import MealFood, Meal, Food


class MealFoodForm(forms.ModelForm):
    class Meta:
        model = MealFood
        fields = ['meal', 'food', 'grams_quantity']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['meal'].queryset = Meal.objects.filter(user=user)
            self.fields['food'].queryset = Food.objects.filter(user=user)
