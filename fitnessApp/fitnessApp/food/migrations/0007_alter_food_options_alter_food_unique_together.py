# Generated by Django 5.1.5 on 2025-01-18 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0006_alter_meal_unique_together'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='food',
            options={'ordering': ['name']},
        ),
        migrations.AlterUniqueTogether(
            name='food',
            unique_together={('name', 'user')},
        ),
    ]
