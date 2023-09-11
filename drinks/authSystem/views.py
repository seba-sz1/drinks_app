from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.models import User

def temp_home(request):
    return render(request, 'temp_home.html')

#TO DO: dodać sprawdzanie maila (czy to mail), walidację hasła
def register(request):
    if request.method == 'GET':
        return render(request,'register.html', {'form': RegisterForm()})
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            usernameTaken = User.objects.filter(username=username).exists()
            emailTaken = User.objects.filter(email=email).exists()
            if emailTaken:
                error = 'This email is already taken. Try again.'
            if usernameTaken:
                error = 'This username is already taken. Try again.'
            if not emailTaken and not usernameTaken:
                user = User.objects.create_user(username, email, password1)
                return render(request, 'temp_home.html')
        else:
            error = 'Wrong password. Try again'

        return render(request, 'register.html', {'error': error, 'form': RegisterForm()})


