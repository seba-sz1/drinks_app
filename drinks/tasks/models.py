from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=220)
    quantity = models.CharField(max_length=50, blank=True, null=True)  # 400
    unit = models.CharField(max_length=50, blank=True, null=True)  # ml, l, szt


class Drinks(models.Model):
    drinkName = models.CharField(max_length=100, blank=False)
    ingredients = models.ManyToManyField(Ingredient, blank=True)
    amount = models.IntegerField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.TextField(blank=True)
    createDate = models.DateTimeField(auto_now_add=True, null=True)


