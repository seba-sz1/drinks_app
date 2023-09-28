from django.test.testcases import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from cocktails.models import Ingredient


class TestIngredient(TestCase):

    def setUp(self):
        self.name = 'test'
        self.amount = 2
        self.unit = 'ml'
        self.valid_ingredient = {
            'name': self.name,
            'amount': self.amount,
            'unit': self.unit,
        }

    def test_ingredient_created_correctly(self):
        ingredient_created = Ingredient.objects.create(name=self.name, amount=self.amount, unit=self.unit)
        self.assertTrue(isinstance(ingredient_created, Ingredient))
        ingredient_from_db = Ingredient.objects.filter(name=self.name)
        self.assertEqual(ingredient_from_db[0].name, self.name)
        self.assertEqual(ingredient_from_db[0].amount, self.amount)
        self.assertEqual(ingredient_from_db[0].unit, self.unit)
        ingredients = Ingredient.objects.all()
        self.assertEqual(ingredients.count(), 1)

    def test_ingredient_with_negative_amount_not_created(self):
        with self.assertRaises(IntegrityError):
            Ingredient.objects.create(name=self.name, amount=-1, unit=self.unit)
            ingredients = Ingredient.objects.all()
            self.assertEqual(ingredients.count(), 0)

    def test_ingredient_with_incorrect_amount_max_validator(self):
            ingredient = Ingredient.objects.create(name=self.name, amount=400, unit=self.unit)
            self.assertRaises(ValidationError, ingredient.full_clean)

    def test_ingredient_with_incorrect_amount_min_validator(self):
            ingredient = Ingredient.objects.create(name=self.name, amount=0, unit=self.unit)
            self.assertRaises(ValidationError, ingredient.full_clean)






