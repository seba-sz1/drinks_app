from django.shortcuts import render
from .models import Drink
from django.utils import timezone


def home(request):
    last_added_cocktails = Drink.objects.order_by('-creation_date')[:6]
    first_half = last_added_cocktails[:3]
    second_half = last_added_cocktails[3:]

    return render(request, 'home.html',
                  {'last_cocktails1': first_half, 'last_cocktails2': second_half})
