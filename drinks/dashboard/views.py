from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cocktails.models import Drink, Ingredient
from .forms import AddDrink


@login_required()
def dashboard(request):
    drinksUser = Drink.objects.filter(owner=request.user)
    ingredients = Ingredient.objects.all()
    return render(request, 'dashboard.html', {'drinksUser': drinksUser, 'ingredients': ingredients})


@login_required()
def create(request):
    if request.method == 'GET':
        return render(request, 'create.html', {'form' : AddDrink()})
    else:
        form = AddDrink(request.POST)
        if form.is_valid():
            drink = form.save(commit=False)
            drink.owner = request.user
            drink.save()
            return redirect('dashboard')
        else:
            error = 'Coś poszło nie tak!'
            return render(request, 'create.html', {'form': AddDrink(), 'error': error})