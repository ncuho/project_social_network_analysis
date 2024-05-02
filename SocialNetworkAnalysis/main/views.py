from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .account.forms import LoginForm
from .models import Link

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
        user_form = UserCreationForm(request.POST)
        # print(user_form.is_valid())
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            # print(username, password)
            user = authenticate(username=username, password=password)
            login(request, user)
            return JsonResponse({'data': "вы зарегистрировались", 'session_id': request.session.session_key},
                                status=200)
        else:
            JsonResponse({'data': "вы не зарегистрировались"}, status=403)
    else:
        user_form = UserCreationForm()
    return render(request, 'main/register.html', {'user_form': user_form})

def get_links_by_user(user_id):
        links = Link.objects.filter(user_id=user_id)
        return list(links)

def get_links_view(request):
    user_id = request.user.id
    links = get_links_by_user(user_id)
    print(links)
    data = {
        "links": links
    }
    return JsonResponse(data)

def remove_link(user_id, link_to_remove):
    user_links = Link.objects.filter(user_id=user_id, link=link_to_remove)
    if user_links.exists():
        user_links.delete()
        return True
    else:
        return False

def delete_links_by_user(request, link):
    user_id = request.user.id
    return remove_link(user_id, link)


