from django import forms
from cocktails.models import Drink, Ingredient

class AddDrink(forms.ModelForm):
    name = forms.CharField(
        label='Nazwa drinka',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    description = forms.CharField(
        label='Krótki opis',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    ingredients_query = Ingredient.objects.all()
    INGREDIENT_CHOICES = [(ingredient.name, ingredient.name) for ingredient in ingredients_query]

    ingredients = forms.MultipleChoiceField(
        label='Wybierz składniki',
        choices=INGREDIENT_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox-class'}),
    )


    image=forms.ImageField(
        label='Dodaj zdjęcie',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),

    )

    drink_publish = forms.BooleanField(
        label='Drink publiczny',
        required=False,  # Jeśli pole ma być opcjonalne
        widget=forms.CheckboxInput(attrs={'class': 'custom-checkbox-class'}),
    )
    class Meta:
        model = Drink
        exclude = ('creation_date', 'owner', 'thumbnail')


