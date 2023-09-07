from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Drinks(models.Model):
    drinkName = models.CharField(max_length=100, blank=False)
    amount = models.IntegerField
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.TextField(blank=True)
    createDate = models.DateTimeField(auto_now_add=True, null=True)
