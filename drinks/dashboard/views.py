import os


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cocktails.models import Drink, Ingredient
from django.http import HttpResponseNotAllowed
from .forms import AddDrink
from django.http import Http404
from django.contrib import messages



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
            if 'image' in request.FILES:
                drink.image = request.FILES['image']

            drink.owner = request.user



            drink.save()  # Zapisz drinka do bazy danych

            selected_ingredients = []
            # Obsłuż składniki
            for key, value in request.POST.items():
                if key.startswith('ingredient_'):
                    ingredient_id = int(key.split('_')[1])

                    selected_ingredients.append(ingredient_id)

                    post_data_list = list(request.POST.items())
                    for key, value in post_data_list:
                        print(f'Klucz: {key}, Wartość: {value}')

                    # Sprawdź, czy użytkownik wprowadził nowy składnik
                    if key.startswith('new_ingredient'):
                        new_ingredient_name = request.POST.get('new_ingredient')
                        new_ingredient_amount = request.POST.get('new_ingredient_amount')
                        new_ingredient_unit = request.POST.get('new_ingredient_unit')


                        if new_ingredient_name:
                            # Utwórz nowy składnik
                            new_ingredient = Ingredient(
                                name=new_ingredient_name,
                                amount=new_ingredient_amount,
                                unit=new_ingredient_unit,
                            )
                            new_ingredient.save()
                            selected_ingredients.append(new_ingredient.id)

            # Przypisz składniki do drinka
            drink.ingredients.set(selected_ingredients)
            return redirect('dashboard')

        else:
            error = 'Coś poszło nie tak!'
            return render(request, 'create.html', {'form': form, 'error': error})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


@login_required()
def delete_drink(request, postId):
    try:
        drink = Drink.objects.get(pk=postId)
        os.remove(drink.image.path)
        os.remove(drink.thumbnail.path)

        drink.delete()

        messages.success(request, 'Drink został usunięty z twojej listy')

        return redirect('dashboard')

    except Drink.DoesNotExist:
        raise Http404("Wpis nie istnieje")

