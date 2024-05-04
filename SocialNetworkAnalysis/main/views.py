from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .account.forms import LoginForm


# from .models import Link


def index(request):
    # print(Link.objects.all());
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ("login", request.path))
    if request.method == 'POST':
        user = User.objects.all()
        # print(user)
        return render(request, 'main/index.html', {'result': "Hello World!"})
    return render(request, 'main/index.html')


def login_views(request):
    if request.method == 'POST':
        # print(User.objects.all())
        login_s = request.GET.get("login", "")
        pas = request.GET.get("pas", "")
        print(login_s, pas)
        user = authenticate(username=login_s, password=pas)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({'data': "вы зарегистрировались", 'session_id': request.session.session_key},
                                    status=200)
            else:
                return JsonResponse({'data': "вы не зарегистрировались"}, status=403)
        else:
            return JsonResponse({'data': "вы не зарегистрировались"}, status=403)
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})


def regist_views(request):
    if request.method == 'POST':
        login_s = request.GET.get("login", "")
        pas = request.GET.get("pas", "")
        if len(User.objects.all().filter(username=login_s)) == 0:
            user = User.objects.create_user(username=login_s, email="lennon@thebeatles.com", password=pas)
            user.save()
            user = authenticate(username=login_s, password=pas)
            login(request, user)
            return JsonResponse({'data': "вы зарегистрировались", 'session_id': request.session.session_key},
                                status=200)
        else:
            return JsonResponse({'data': "вы не зарегистрировались"}, status=402)
    else:
        return JsonResponse({'data': "вы не зарегистрировались"}, status=403)
