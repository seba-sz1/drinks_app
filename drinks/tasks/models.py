from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Ingredient(models.Model):
    name = models.CharField(max_length=220)
    amount_choices = (('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9),
                      ('10', 10), ('15', 15), ('20', 20), ('25', 25), ('30', 30), ('35', 35), ('40', 40),
                      ('45', 45), ('50', 50), ('60', 60), ('70', 70), ('80', 80), ('90', 90), ('100', 100),
                      ('110', 110), ('120', 120), ('130', 130), ('140', 140), ('150', 150), ('160', 160), ('170', 170),
                      ('180', 180), ('190', 190), ('200', 200), ('210', 210), ('220', 220), ('230', 230), ('240', 240),
                      ('250', 250), ('260', 260), ('270', 270), ('280', 280), ('290', 290), ('300', 300))
    ingredient_amount = models.PositiveIntegerField(default=1,
                                                    validators=[MinValueValidator(1)],
                                                    choices=amount_choices,
                                                    blank=True)
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
