import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .account.forms import LoginForm
from .models import Link, UserInfo
from .parser.parser import User_pars


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

    def get_links_by_user(user_id):
        links = Link.objects.filter(user_id=user_id)
        return list(links)


def get_links_by_user(user_id):
    links = Link.objects.filter(user_id=user_id)
    return str(links)


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


def add_link(user_id, link_to_add):
    user_links = Link(user_id=user_id, link=link_to_add)
    user_links.save()
    return True


def add_links_by_user(request):
    link = request.GET.get("link", "")
    user_id = request.user.id
    if add_link(user_id, link):
        return JsonResponse({'data': "вы добавили ссылку"}, status=200)
    else:
        return JsonResponse({'data': "вы не добавили ссылку"}, status=403)


def add_info_by_links(request):
    link_base = request.GET.get("link", "")
    link = link_base.split("/")[len(link_base.split("/")) - 1]
    link_osn = Link.objects.filter(link=link_base)

    if (len(UserInfo.objects.filter(link_id=link_osn[0].id)) > 0):
        return JsonResponse(json.loads(json.dumps(UserInfo.objects.filter(link_id=link_osn[0].id)[0].get_info)),
                            status=200)
    else:
        newUser = User_pars(link)
        status = [1]
        status[0] = newUser.main_info()

        is_closed = status[0]["is_closed"]
        bdate = status[0]['bdate']
        if len(bdate.split('.')) == 3:
            if len(bdate.split('.')[0]) == 1 and len(bdate.split('.')[1]) == 1:
                bdate = '0' + bdate.split('.')[0] + '.' + '0' + bdate.split('.')[1] + '.' + bdate.split('.')[2]
            elif len(bdate.split('.')[0]) == 1 and len(bdate.split('.')[1]) == 2:
                bdate = '0' + bdate.split('.')[0] + '.' + bdate.split('.')[1] + '.' + bdate.split('.')[2]
            elif len(bdate.split('.')[0]) == 2 and len(bdate.split('.')[1]) == 1:
                bdate = bdate.split('.')[0] + '.' + '0' + bdate.split('.')[1] + '.' + bdate.split('.')[2]
        elif len(bdate.split('.')) == 2:
            if len(bdate.split('.')[0]) == 1 and len(bdate.split('.')[1]) == 1:
                bdate = '0' + bdate.split('.')[0] + '.' + '0' + bdate.split('.')[1]
            elif len(bdate.split('.')[0]) == 1 and len(bdate.split('.')[1]) == 2:
                bdate = '0' + bdate.split('.')[0] + '.' + bdate.split('.')[1]
            elif len(bdate.split('.')[0]) == 2 and len(bdate.split('.')[1]) == 1:
                bdate = bdate.split('.')[0] + '.' + '0' + bdate.split('.')[1]

        user_id = status[0]['id']
        is_account_closed = 'закрыт' if is_closed else 'открыт'
        first_name = status[0].get('first_name', 'нет информации')
        last_name = status[0].get('last_name', 'нет информации')
        bdate = 'нет информации' if status[0]['bdate'] == '' else bdate
        status_text = 'нет информации' if status[0]['status'] == '' else status[0]['status']
        country = 'нет информации' if status[0]['country'] == '' else status[0]['country']['title']
        city = 'нет информации' if status[0]['city'] == '' else status[0]['city']['title']
        home_town = 'нет информации' if status[0]['home_town'] == '' else status[0]['home_town']
        university = 'нет информации' if status[0]['university_name'] == '' else status[0]['university_name']
        faculty = 'нет информации' if status[0]['faculty_name'] == '' else status[0]['faculty_name']
        graduation = 'нет информации' if status[0]['graduation'] == 0 else status[0]['graduation']
        education_form = 'нет информации' if 'education_form' not in status[0] else status[0]['education_form']
        education_status = 'нет информации' if 'education_status' not in status[0] else status[0]['education_status']
        followers_count = 'нет информации' if 'followers_count' not in status[0] else status[0]['followers_count']
        crop_photo = 'нет информации' if status[0]['crop_photo'] == '' else \
            status[0]['crop_photo']['photo']['sizes'][-1]['url']
        activities = 'нет информации' if status[0]['activities'] == '' else status[0]['activities']
        interests = 'нет информации' if status[0]['interests'] == '' else status[0]['interests']
        books = 'нет информации' if status[0]['books'] == '' else status[0]['books']
        games = 'нет информации' if status[0]['games'] == '' else status[0]['games']
        movies = 'нет информации' if status[0]['movies'] == '' else status[0]['movies']
        music = 'нет информации' if status[0]['music'] == '' else status[0]['music']
        quotes = 'нет информации' if status[0]['quotes'] == '' else status[0]['quotes']
        verified = 'Страница верифицирована' if status[0]['verified'] == '1' else 'Страница не верифицирована'
        albums = 'нет информации' if 'albums' not in status[0]['counters'] else status[0]['counters']['albums']
        audios = 'нет информации' if 'audios' not in status[0]['counters'] else status[0]['counters']['audios']
        friends = 'нет информации' if 'friends' not in status[0]['counters'] else status[0]['counters']['friends']
        gifts = 'нет информации' if 'gifts' not in status[0]['counters'] else status[0]['counters']['gifts']
        groups = 'нет информации' if 'groups' not in status[0]['counters'] else status[0]['counters']['groups']
        photos = 'нет информации' if 'photos' not in status[0]['counters'] else status[0]['counters']['photos']
        subscriptions_on_profiles = 'нет информации' if 'subscriptions' not in status[0]['counters'] else \
            status[0]['counters']['subscriptions']
        videos = 'нет информации' if 'videos' not in status[0]['counters'] else status[0]['counters']['videos']
        length_posts = 'нет информации' if 'posts' not in status[0]['counters'] else status[0]['counters']['posts']
        inspired_by = 'нет информации' if 'inspired_by' not in status[0]['personal'] else status[0]['personal'][
            'inspired_by']
        langs = 'нет информации' if 'langs' not in status[0]['personal'] else ', '.join(status[0]['personal']['langs'])
        religion = 'нет информации' if 'religion' not in status[0]['personal'] else status[0]['personal']['religion']
        if 'schools' not in status[0]:
            schools = 'нет информации\n'
        else:
            schools = ''
            for school in range(len(status[0]['schools'])):
                schools += f"{status[0]['schools'][school]['name']}\n"

        user_info = UserInfo(username=link, user_id=user_id, is_account_closed=is_account_closed, first_name=first_name,
                             last_name=last_name, bdate=bdate, status_text=status_text, country=country, city=city,
                             home_town=home_town,
                             schools=schools, university=university, faculty=faculty, graduation=graduation,
                             education_form=education_form, education_status=education_status, langs=langs,
                             friends=friends,
                             followers_count=followers_count, crop_photo=crop_photo, albums=albums, audios=audios,
                             gifts=gifts,
                             groups=groups, photos=photos, subscriptions_on_profiles=subscriptions_on_profiles,
                             videos=videos,
                             length_posts=length_posts, activities=activities, interests=interests, religion=religion,
                             books=books,
                             games=games, movies=movies, music=music, quotes=quotes, inspired_by=inspired_by,
                             verified=verified, link_id=link_osn[0].id)
        user_info.save()
        return JsonResponse(json.loads(json.dumps(user_info.get_info)), status=200)
