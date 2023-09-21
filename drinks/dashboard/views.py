from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cocktails.models import Drink


@login_required()
def dashboard(request):
    drinksUser = Drink.objects.filter(owner=request.user)
    return render(request, 'dashboard.html', {'drinksUser': drinksUser})