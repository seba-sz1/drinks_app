from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Ingredient(models.Model):
    name = models.CharField(max_length=220)
    ingredient_amount = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], blank=True)
    ml, szt = 'ml', 'szt'
    unit_choices = [(ml, 'mililitry'), (szt, 'sztuk')]
    unit = models.CharField(default=ml, choices=unit_choices, max_length=3)

    def __str__(self):
        return f'{self.name}  |  {self.ingredient_amount} {self.unit}'


class Drink(models.Model):
    drink_name = models.CharField(max_length=100, blank=False)
    ingredients = models.ManyToManyField(Ingredient, blank=True)
    amount = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.drink_name} | {self.creation_date} | {self.description}'
