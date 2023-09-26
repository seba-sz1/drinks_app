from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('<int:drinkID>/', views.detail_cocktail, name='detail_cocktail'),
]
