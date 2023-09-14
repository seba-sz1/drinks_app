from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect

from .forms import LoginForm
from .forms import RegisterForm


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'form': RegisterForm()})
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if not form.is_valid():
            error = form.errors
        elif User.objects.filter(email=form.cleaned_data['email']).exists():
            error = 'Ten email jest już zajęty. Spróbuj ponownie.'
        else:
            try:
                user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'],
                                                form.cleaned_data['password1'])
                return redirect("home")
            except IntegrityError as e:
                error = e
        return render(request, 'register.html', {'error': error, 'form': RegisterForm()})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def login_user(request):
    if request.method == 'GET':
        return render(request, 'login_user.html', {'form': LoginForm()})
    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                error = 'Błąd autentykacji..'
        else:
            error = form.errors
        return render(request, 'login_user.html', {'error': error, 'form': AuthenticationForm()})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


@login_required
def logout_user(request):
    logout(request)
    return redirect("home")


@login_required()
def change_password(request):
    if request.method == "GET":
        form = PasswordChangeForm(request.user)
    elif request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Hasło zostało pomyślnie zaktualizowane.')
            return redirect("home")
        else:
            messages.error(request, 'Coś poszło nie tak. Popraw poniższe błędy.')
    else:
        error = 'Coś poszło nie tak.'
    return render(request, "change_password.html", {'form': form})


