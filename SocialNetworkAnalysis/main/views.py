from collections import Counter
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from langchain_community.chat_models.gigachat import GigaChat
from langchain_core.messages import SystemMessage, HumanMessage
from vk_api import ApiError

from .account.forms import LoginForm
from .models import Link, UserInfo
from .parser.parser import User_pars
import nltk

nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
import argostranslate.package
import argostranslate.translate


def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ("login", request.path))
    if request.method == 'POST':
        return render(request, 'main/index.html', {'result': "Hello World!"})
    return render(request, 'main/index.html')


def login_views(request):
    if request.method == 'POST':
        login_s = request.GET.get("login", "")
        pas = request.GET.get("pas", "")
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
    session_id = request.GET.get("session_id", "")
    session = Session.objects.get(session_key=session_id)
    session_data = session.get_decoded()
    uid = session_data.get('_auth_user_id')
    links = get_links_by_user(uid)
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
    user_links = Link.objects.create(user_id=user_id, link=link_to_add)
    user_links.save()
    return user_links


def add_links_by_user(request):
    link = request.GET.get("link", "")
    session_id = request.GET.get("session_id", "")
    session = Session.objects.get(session_key=session_id)
    session_data = session.get_decoded()
    uid = session_data.get('_auth_user_id')
    if add_link(uid, link):
        return JsonResponse({'data': "вы добавили ссылку"}, status=200)
    else:
        return JsonResponse({'data': "вы не добавили ссылку"}, status=403)


def get_frends_by_link_for_bd(request):
    link_base = request.GET.get("link", "")
    link = link_base.split("/")[len(link_base.split("/")) - 1]
    link_osn = Link.objects.filter(link=link_base)
    if len(link_osn) == 0:
        session_id = request.GET.get("session_id", "")
        session = Session.objects.get(session_key=session_id)
        session_data = session.get_decoded()
        uid = session_data.get('_auth_user_id')
        link_osn = [1]
        link_osn[0] = add_link(uid, link_base)
    if (len(UserInfo.objects.filter(link_id=link_osn[0].id)) > 0):
        user_info = UserInfo.objects.filter(link_id=link_osn[0].id)[0]
        if user_info.frends_data is None or user_info.frends_data == '':
            print(user_info.frends_data, user_info.frends_data)
            return JsonResponse({"data": ""}, status=202)
        id_user_frends = user_info.frends_data.split("\n")
        mas_rez = []
        for i in id_user_frends:
            if (len(UserInfo.objects.filter(user_id=i.split(")")[0])) > 0):
                mas_rez.append(i)
        return JsonResponse({"data": "\n".join(mas_rez)},
                            status=200)
    return JsonResponse({"data": "Такого пользователя нету"}, status=201)


def add_info_by_links(request):
    link_base = request.GET.get("link", "")
    link = link_base.split("/")[len(link_base.split("/")) - 1]
    link_osn = Link.objects.filter(link=link_base)

    if len(link_osn) == 0:
        session_id = request.GET.get("session_id", "")
        session = Session.objects.get(session_key=session_id)
        session_data = session.get_decoded()
        uid = session_data.get('_auth_user_id')
        link_osn = [add_link(uid, link_base)]

    if (len(UserInfo.objects.filter(link_id=link_osn[0].id)) > 0):
        return JsonResponse({"data": UserInfo.objects.filter(link_id=link_osn[0].id)[0].get_info},
                            status=200)
    else:
        try:
            newUser = User_pars(link)
            status = [1]
            status[0] = newUser.main_info()
        except ApiError:
            return JsonResponse({"data": "Акаунт закрыт"}, status=201)

        is_closed = status[0]["is_closed"]
        if 'bdate' in status[0]:
            bdate = status[0]['bdate']
        else:
            bdate = 'нет информации'
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
        if 'bdate' in status[0]:
            bdate = 'нет информации' if status[0]['bdate'] == '' else bdate
        else:
            bdate = 'нет информации'
        if 'status' in status[0]:
            status_text = 'нет информации' if status[0]['status'] == '' else status[0]['status']
        else:
            status_text = 'нет информации'
        if 'country' in status[0]:
            country = 'нет информации' if status[0]['country'] == '' else status[0]['country']['title']
        else:
            country = 'нет информации'
        if 'city' in status[0]:
            city = 'нет информации' if status[0]['city'] == '' else status[0]['city']['title']
        else:
            city = 'нет информации'
        if 'home_town' in status[0]:
            home_town = 'нет информации' if status[0]['home_town'] == '' else status[0]['home_town']
        else:
            home_town = 'нет информации'
        if 'university' in status[0]:
            university = 'нет информации' if status[0]['university_name'] == '' else status[0]['university_name']
        else:
            university = 'нет информации'
        if 'faculty' in status[0]:
            faculty = 'нет информации' if status[0]['faculty_name'] == '' else status[0]['faculty_name']
        else:
            faculty = 'нет информации'
        if 'graduation' in status[0]:
            graduation = 'нет информации' if status[0]['graduation'] == 0 else status[0]['graduation']
        else:
            graduation = 'нет информации'
        if 'education_form' in status[0]:
            education_form = 'нет информации' if 'education_form' not in status[0] else status[0]['education_form']
        else:
            education_form = 'нет информации'
        if 'education_status' in status[0]:
            education_status = 'нет информации' if 'education_status' not in status[0] else status[0][
                'education_status']
        else:
            education_status = 'нет информации'
        if 'followers_count' in status[0]:
            followers_count = 'нет информации' if 'followers_count' not in status[0] else status[0]['followers_count']
        else:
            followers_count = 'нет информации'
        if 'crop_photo' in status[0]:
            crop_photo = 'нет информации' if status[0]['crop_photo'] == '' else \
                status[0]['crop_photo']['photo']['sizes'][-1]['url']
        else:
            crop_photo = 'нет информации'
        if 'activities' in status[0]:
            activities = 'нет информации' if status[0]['activities'] == '' else status[0]['activities']
        else:
            activities = 'нет информации'
        if 'interests' in status[0]:
            interests = 'нет информации' if status[0]['interests'] == '' else status[0]['interests']
        else:
            interests = 'нет информации'
        if 'books' in status[0]:
            books = 'нет информации' if status[0]['books'] == '' else status[0]['books']
        else:
            books = 'нет информации'
        if 'games' in status[0]:
            games = 'нет информации' if status[0]['games'] == '' else status[0]['games']
        else:
            games = 'нет информации'
        if 'movies' in status[0]:
            movies = 'нет информации' if status[0]['movies'] == '' else status[0]['movies']
        else:
            movies = 'нет информации'
        if 'music' in status[0]:
            music = 'нет информации' if status[0]['music'] == '' else status[0]['music']
        else:
            music = 'нет информации'
        if 'quotes' in status[0]:
            quotes = 'нет информации' if status[0]['quotes'] == '' else status[0]['quotes']
        else:
            quotes = 'нет информации'
        if 'verified' in status[0]:
            verified = 'Страница верифицирована' if status[0]['verified'] == '1' else 'Страница не верифицирована'
        else:
            verified = 'нет информации'
        if 'albums' in status[0]:
            albums = 'нет информации' if 'albums' not in status[0]['counters'] else status[0]['counters']['albums']
        else:
            albums = 'нет информации'
        if 'audios' in status[0]:
            audios = 'нет информации' if 'audios' not in status[0]['counters'] else status[0]['counters']['audios']
        else:
            audios = 'нет информации'
        if 'friends' in status[0]:
            friends = 'нет информации' if 'friends' not in status[0]['counters'] else status[0]['counters']['friends']
        else:
            friends = 'нет информации'
        if 'gifts' in status[0]:
            gifts = 'нет информации' if 'gifts' not in status[0]['counters'] else status[0]['counters']['gifts']
        else:
            gifts = 'нет информации'
        if 'groups' in status[0]:
            groups = 'нет информации' if 'groups' not in status[0]['counters'] else status[0]['counters']['groups']
        else:
            groups = 'нет информации'
        if 'photos' in status[0]:
            photos = 'нет информации' if 'photos' not in status[0]['counters'] else status[0]['counters']['photos']
        else:
            photos = 'нет информации'
        if 'subscriptions_on_profiles' in status[0]:
            subscriptions_on_profiles = 'нет информации' if 'subscriptions' not in status[0]['counters'] else \
                status[0]['counters']['subscriptions']
        else:
            subscriptions_on_profiles = 'нет информации'
        if 'videos' in status[0]:
            videos = 'нет информации' if 'videos' not in status[0]['counters'] else status[0]['counters']['videos']
        else:
            videos = 'нет информации'
        if 'length_posts' in status[0]:
            length_posts = 'нет информации' if 'posts' not in status[0]['counters'] else status[0]['counters']['posts']
        else:
            length_posts = 'нет информации'
        if 'inspired_by' in status[0]:
            inspired_by = 'нет информации' if 'inspired_by' not in status[0]['personal'] else status[0]['personal'][
                'inspired_by']
        else:
            inspired_by = 'нет информации'
        if 'langs' in status[0]:
            langs = 'нет информации' if 'langs' not in status[0]['personal'] else ', '.join(
                status[0]['personal']['langs'])
        else:
            langs = 'нет информации'
        if 'religion' in status[0]:
            religion = 'нет информации' if 'religion' not in status[0]['personal'] else status[0]['personal'][
                'religion']
        else:
            religion = 'нет информации'
        if 'schools' not in status[0]:
            schools = 'нет информации\n'
        else:
            schools = ''
            for school in range(len(status[0]['schools'])):
                schools += f"{status[0]['schools'][school]['name']}\n"
        try:
            user_info = UserInfo.objects.create(username=link, user_id=user_id, is_account_closed=is_account_closed,
                                                first_name=first_name,
                                                last_name=last_name, bdate=bdate, status_text=status_text,
                                                country=country,
                                                city=city,
                                                home_town=home_town,
                                                schools=schools, university=university, faculty=faculty,
                                                graduation=graduation,
                                                education_form=education_form, education_status=education_status,
                                                langs=langs,
                                                friends=friends,
                                                followers_count=followers_count, crop_photo=crop_photo, albums=albums,
                                                audios=audios,
                                                gifts=gifts,
                                                groups=groups, photos=photos,
                                                subscriptions_on_profiles=subscriptions_on_profiles,
                                                videos=videos,
                                                length_posts=length_posts, activities=activities, interests=interests,
                                                religion=religion,
                                                books=books,
                                                games=games, movies=movies, music=music, quotes=quotes,
                                                inspired_by=inspired_by,
                                                verified=verified, link_id=link_osn[0].id,
                                                frends_data='\n'.join(newUser.friends()))
            user_info.save()
        except ApiError:
            return JsonResponse({"data": "Акаунт закрыт"}, status=201)


        return JsonResponse({"data": user_info.get_info}, status=200)


chat = GigaChat(
    credentials='OTk3NTBiMzctYWE1MC00MDQ1LWIzZWMtODY3YzQxZGIyZDAwOjM4NjkxOGY2LTM4YjYtNGM3OC1hZTBkLTIxN2M4YmVhMjQ5Mg==',
    verify_ssl_certs=False)


def giga_chat_ai(request):
    text = request.GET.get("text", "")
    messages = [
        SystemMessage(
            content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы."
        )
    ]
    messages.append(HumanMessage(content=text))
    res = chat(messages)
    messages.append(res)
    return JsonResponse({'data': res.content}, status=200)


def giga_chat_ai_get_info(request):
    link_base = request.GET.get("link", "")
    link_osn = Link.objects.filter(link=link_base)
    messages = [
        SystemMessage(
            content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы. Тебе надо дать наиболее понятный и короткий ответ с примером."
        )
    ]
    if len(link_osn) == 0:
        session_id = request.GET.get("session_id", "")
        session = Session.objects.get(session_key=session_id)
        session_data = session.get_decoded()
        uid = session_data.get('_auth_user_id')
        link_osn = [1]
        link_osn[0] = add_link(uid, link_base)

    if (len(UserInfo.objects.filter(link_id=link_osn[0].id)) > 0):
        info = UserInfo.objects.filter(link_id=link_osn[0].id)[0].get_info
        mas_fact = []
        text = "Дай подробный психологический портрет человеком о котором известно: "
        if info["status_text"] != 'нет информации':
            mas_fact.append("статус в вк " + info["status_text"])
        if info["first_name"] != 'нет информации':
            mas_fact.append("имя в соц сетях " + info["first_name"])
        if info["last_name"] != 'нет информации':
            mas_fact.append("фамилия в соц сетях " + info["last_name"])
        if info["country"] != 'нет информации':
            mas_fact.append("живет в стране " + info["country"])
        if info["city"] != 'нет информации':
            mas_fact.append("живет в городе " + info["city"])
        if info["home_town"] != 'нет информации':
            mas_fact.append("родился в городе " + info["home_town"])
        if info["university"] != 'нет информации':
            mas_fact.append("учился в институте " + info["university"])
        if info["faculty"] != 'нет информации':
            mas_fact.append("учился в институте на факультете " + info["faculty"])
        if info["activities"] != 'нет информации':
            mas_fact.append("занимется " + info["activities"])
        if info["interests"] != 'нет информации':
            mas_fact.append("интересуется " + info["interests"])
        if info["religion"] != 'нет информации':
            mas_fact.append("религия " + info["religion"])
        if info["books"] != 'нет информации':
            mas_fact.append("любимые книги " + info["books"])
        if info["games"] != 'нет информации':
            mas_fact.append("любимые игры " + info["games"])
        if info["movies"] != 'нет информации':
            mas_fact.append("любимые фильмы " + info["movies"])
        if info["music"] != 'нет информации':
            mas_fact.append("любимая музыка " + info["music"])
        if info["quotes"] != 'нет информации':
            mas_fact.append("любимые цитаты " + info["quotes"])
        if info["inspired_by"] != 'нет информации':
            mas_fact.append("вдохновляет " + info["inspired_by"])
        text += ",".join(mas_fact) + "."
        text += "Также напиши рекомендации по знакомству, убеждению, налаживанию доверительных отношений с этим человеком. Дай короткое описание этого пользователя."
        if len(mas_fact) > 2:
            messages.append(HumanMessage(content=text))
            res = chat(messages)
            messages.append(res)
            print(res.content)
            return JsonResponse({'data': res.content}, status=200)
        else:
            return JsonResponse({'data': "Недостаточно данных для анализа"}, status=201)
    else:
        return JsonResponse({'data': "Данных о пользователе нет в базе данных"}, status=403)


def giga_chat_ai_connect_info(request):
    link_base = request.GET.get("link", "")
    link_osn = Link.objects.filter(link=link_base)
    messages = [
        SystemMessage(
            content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы. Тебе надо дать наиболее понятный и короткий ответ с примером."
        )
    ]
    if len(link_osn) == 0:
        session_id = request.GET.get("session_id", "")
        session = Session.objects.get(session_key=session_id)
        session_data = session.get_decoded()
        uid = session_data.get('_auth_user_id')
        link_osn = [1]
        link_osn[0] = add_link(uid, link_base)

    if (len(UserInfo.objects.filter(link_id=link_osn[0].id)) > 0):
        info = UserInfo.objects.filter(link_id=link_osn[0].id)[0].get_info
        mas_fact = []
        text = "Дай короткие и максимально эффективные рекомендации по знакомству с человеком о котором известно: "
        if info["status_text"] != 'нет информации':
            mas_fact.append("статус в вк " + info["status_text"])
        if info["first_name"] != 'нет информации':
            mas_fact.append("имя в соц сетях " + info["first_name"])
        if info["last_name"] != 'нет информации':
            mas_fact.append("фамилия в соц сетях " + info["last_name"])
        if info["country"] != 'нет информации':
            mas_fact.append("живет в стране " + info["country"])
        if info["city"] != 'нет информации':
            mas_fact.append("живет в городе " + info["city"])
        if info["home_town"] != 'нет информации':
            mas_fact.append("родился в городе " + info["home_town"])
        if info["university"] != 'нет информации':
            mas_fact.append("учился в институте " + info["university"])
        if info["faculty"] != 'нет информации':
            mas_fact.append("учился в институте на факультете " + info["faculty"])
        if info["activities"] != 'нет информации':
            mas_fact.append("занимется " + info["activities"])
        if info["interests"] != 'нет информации':
            mas_fact.append("интересуется " + info["interests"])
        if info["religion"] != 'нет информации':
            mas_fact.append("религия " + info["religion"])
        if info["books"] != 'нет информации':
            mas_fact.append("любимые книги " + info["books"])
        if info["games"] != 'нет информации':
            mas_fact.append("любимые игры " + info["games"])
        if info["movies"] != 'нет информации':
            mas_fact.append("любимые фильмы " + info["movies"])
        if info["music"] != 'нет информации':
            mas_fact.append("любимая музыка " + info["music"])
        if info["quotes"] != 'нет информации':
            mas_fact.append("любимые цитаты " + info["quotes"])
        if info["inspired_by"] != 'нет информации':
            mas_fact.append("вдохновляет " + info["inspired_by"])
        text += ",".join(mas_fact) + "."
        if len(mas_fact) > 2:
            messages.append(HumanMessage(content=text))
            res = chat(messages)
            messages.append(res)
            print(res.content)
            return JsonResponse({'data': res.content}, status=200)
        else:
            return JsonResponse({'data': "Недостаточно данных для анализа"}, status=200)
    else:
        return JsonResponse({'data': "Данных о пользователе нет в базе данных"}, status=403)


def get_info_grafik_worlds(request):
    link_base = request.GET.get("link", "")
    link = link_base.split("/")[len(link_base.split("/")) - 1]
    link_osn = Link.objects.filter(link=link_base)
    if len(link_osn) == 0:
        session_id = request.GET.get("session_id", "")
        session = Session.objects.get(session_key=session_id)
        session_data = session.get_decoded()
        uid = session_data.get('_auth_user_id')
    try:
        newUser = User_pars(link)
        comments = newUser.comments()
    except ApiError:
        return JsonResponse({"data": "Акаунт закрыт"}, status=201)
    words = word_tokenize("\n".join(comments))
    word_freq = Counter(words)
    most_common_words = word_freq.most_common(10)
    return JsonResponse({"data": most_common_words}, status=200)


def sentiment_analysis(text):
    sid = SentimentIntensityAnalyzer()
    print(text)
    sentiment_scores = sid.polarity_scores(text)
    return sentiment_scores


def get_info_grafik_toksik(request):
    link_base = request.GET.get("link", "")
    link = link_base.split("/")[len(link_base.split("/")) - 1]
    link_osn = Link.objects.filter(link=link_base)
    if len(link_osn) == 0:
        session_id = request.GET.get("session_id", "")
        session = Session.objects.get(session_key=session_id)
        session_data = session.get_decoded()
        uid = session_data.get('_auth_user_id')
    try:
        newUser = User_pars(link)
        comments = newUser.comments()
    except ApiError:
        return JsonResponse({"data": "Акаунт закрыт"}, status=201)
    sentiments = []
    from_code = "ru"
    to_code = "en"
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())
    for text in comments:
        translatedText = argostranslate.translate.translate(text, from_code, to_code)
        blob = sentiment_analysis(translatedText)
        sentiments.append(blob["compound"])
    print(sentiments)
    return JsonResponse({"data": sentiments}, status=200)
