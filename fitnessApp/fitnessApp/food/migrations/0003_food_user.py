# Generated by Django 5.1.5 on 2025-01-17 07:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_alter_mealfood_meal'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_foods', to='users.userprofile'),
        ),
    ]
