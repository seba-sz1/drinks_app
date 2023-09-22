from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Ingredient(models.Model):
    unit_type = (('ml', 'mililitry'), ('szt', 'sztuk'))
    name = models.CharField(max_length=220)
    amount = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(300)],
                                         blank=True)
    unit = models.CharField(default='ml', choices=unit_type, max_length=3)

    def __str__(self):
        return f'{self.name}  |  {self.amount} {self.unit}'


class Drink(models.Model):
    name = models.CharField(max_length=100, blank=False)
    ingredients = models.ManyToManyField(Ingredient)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='static/images/', default='static/images/1.jpg')

    def __str__(self):
        return f'{self.name} | {self.creation_date} | {self.description}'
