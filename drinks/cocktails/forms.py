from django import forms
from .models import Drink


class TaskForm(forms.ModelForm):
    class Meta:
        model = Drink
        # fields = ('name','description')
        exludes = ('thumbnail', 'creation_date', 'owner', 'pin_to_main_page')
        # fields = '__all__' # przekazanie wszystkich pól do formularza
