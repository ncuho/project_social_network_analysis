from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .account.forms import LoginForm

def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ("login", request.path))
    if request.method == 'POST':
        user = User.objects.all()
        print(user)
        return render(request, 'main/index.html', {'result': "Hello World!"})
    return render(request, 'main/index.html')

def login_views(request):
    if request.method == 'POST':
        print(User.objects.all())
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})
