from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=220)


class IngredientToRecipeDrink(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.SET_NULL)
    quantity = models.CharField(max_length=50, blank=True, null=True)  # 400
    unit = models.CharField(max_length=50, blank=True, null=True)  # pounds, lbs, oz ,grams, etc
    instructions = models.TextField(blank=True, null=True)


class Drinks(models.Model):
    drinkName = models.CharField(max_length=100, blank=False)
    ingredients = models.ManyToManyField(Ingredient,  blank=True, Null=True, through='IngredientToRecipeDrink')
    amount = models.IntegerField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.TextField(blank=True)
    createDate = models.DateTimeField(auto_now_add=True, null=True)


