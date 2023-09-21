from django import forms
from cocktails.models import Drink

class AddDrink(forms.ModelForm):
    class Meta:
        model = Drink
        exclude = ('creation_date', 'owner')