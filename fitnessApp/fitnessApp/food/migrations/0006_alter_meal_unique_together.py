# Generated by Django 5.1.5 on 2025-01-17 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0005_alter_mealfood_unique_together'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='meal',
            unique_together={('meal_type', 'user')},
        ),
    ]
