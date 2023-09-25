from django.shortcuts import render
from .models import Drink
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def home(request):
    last_added_cocktails = Drink.objects.order_by('-creation_date')[:6]
    first_half = last_added_cocktails[:3]
    second_half = last_added_cocktails[3:]

    return render(request, 'home.html',
                  {'last_cocktails1': first_half, 'last_cocktails2': second_half})


def search(request):
    query = request.GET.get('q')
    drinks = Drink.objects.filter(name__icontains=query)
    total_count = drinks.count()
    last_added_cocktails = Drink.objects.order_by('-creation_date')[:3]

    paginator = Paginator(drinks, 8)
    page_number = request.GET.get('page')

    try:
        drinks = paginator.get_page(page_number)
    except PageNotAnInteger:
        drinks = paginator.page(1)
    except EmptyPage:
        drinks = paginator.page(paginator.num_pages)

    context = {'drinks': drinks, 'last_cocktails': last_added_cocktails, 'query': query, 'total_count': total_count}

    return render(request, 'search_results.html', context)
