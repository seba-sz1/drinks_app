from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cocktails.models import Drink


@login_required()
def dashboard(request):
    # productUser = Drink.objects.filter(user=request.user)
    return render(request, 'dashboard.html')