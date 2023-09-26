from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cocktails.models import Drink, Ingredient
from django.http import HttpResponseNotAllowed
from .forms import AddDrink


@login_required()
def dashboard(request):
    drinksUser = Drink.objects.filter(owner=request.user)
    ingredients = Ingredient.objects.all()
    return render(request, 'dashboard.html', {'drinksUser': drinksUser, 'ingredients': ingredients})


@login_required()
def create(request):
    if request.method == 'GET':
        available_ingredients = Ingredient.objects.all()
        return render(request, 'create.html', {'form': AddDrink(), 'ingredients': available_ingredients})

    elif request.method == 'POST':
        form = AddDrink(request.POST, request.FILES)
        if form.is_valid():
            drink = form.save(commit=False)
            drink.owner = request.user
            drink.save()  # Zapisz drinka do bazy danych

            selected_ingredients = []
            # Obsłuż składniki
            for key, value in request.POST.items():
                if key.startswith('ingredient_'):
                    ingredient_id = int(key.split('_')[1])
                    # ingredient = Ingredient.objects.get(pk=ingredient_id)
                    # selected_ingredient_id = form.cleaned_data['ingredient']
                    # selected_ingredient_id = request.POST.get('ingredient')
                    selected_ingredients.append(ingredient_id)

            # Przypisz składniki do drinka
            drink.ingredients.set(selected_ingredients)
            return redirect('dashboard')

        else:
            error = 'Coś poszło nie tak!'
            return render(request, 'create.html', {'form': form, 'error': error})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])