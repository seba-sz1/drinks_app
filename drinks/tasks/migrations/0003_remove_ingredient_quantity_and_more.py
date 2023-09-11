# Generated by Django 4.2.5 on 2023-09-11 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_drink_ingredient_delete_drinks_drink_ingredients_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='quantity',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='ingredient_amount',
            field=models.PositiveIntegerField(blank=True, default=1),
        ),
    ]
