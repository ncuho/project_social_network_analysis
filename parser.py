import sqlite3
import vk_api
import time
from googletrans import Translator


class User:
    def __init__(self, username):
        self.username = username
        self.access_token = 'vk1.a.ae4PjjbPvm8L5vXH1F-26IEjvSsn8cUbexDNV6QtQ_qjePgHiPN3HNU_UdA_oBU9xSNhA9EWPwLk7gCDvk9g7ydePZHnAJ0Ih_j2TRUY8sLWOQztj3nc_fPyL5DW6Ut3-H4Nv34zvKLu6S4mH57yJAzbdNmFrIP5PK41sebbFP1pB75RaK_y1OvbhbCS7Awe-clGfajGGpziOLNbDSeAug'
        self.session = vk_api.VkApi(token=self.access_token)
        self.vk = self.session.get_api()
        self.first_name = self.session.method("users.get", {"user_id": self.username})[0].get('first_name', 'нет информации')

    def main_info(self):
        if self.first_name == 'DELETED':
            return print("Аккаунт пользователя был удален")

        fields = "activities,about,counters,books,bdate,can_be_invited_group,connections,contacts,city,country,crop_photo,domain,education,exports,followers_count,friend_status,has_photo,has_mobile,home_town,photo_100,photo_200,photo_200_orig,photo_400_orig,photo_50,sex,site,schools,screen_name,status,verified,games,interests,is_favorite,is_friend,is_hidden_from_feed,last_seen,maiden_name,military,movies,music,nickname,occupation,online,personal,photo_id,photo_max,photo_max_orig,quotes,relation,relatives,timezone,tv,universities"
        status = self.session.method("users.get", {"user_id": self.username, "fields": fields})
        if "error" in status:
            print("Ошибка при запросе к API VK")
        is_closed = status[0]["is_closed"]

        try:
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
        except KeyError:
            bdate = 'нет информации'

        user_id = status[0]['id']
        is_account_closed = 'закрыт' if is_closed else 'открыт'
        first_name = status[0].get('first_name', 'нет информации')
        last_name = status[0].get('last_name', 'нет информации')
        try:
            bdate = 'нет информации' if status[0]['bdate'] == '' else bdate
        except KeyError:
            bdate = 'нет информации'
        try:
            status_text = 'нет информации' if status[0]['status'] == '' else status[0]['status']
        except KeyError:
            status_text = 'нет информации'
        try:
            country = 'нет информации' if status[0]['country'] == '' else status[0]['country']['title']
        except KeyError:
            country = 'нет информации'
        try:
            city = 'нет информации' if status[0]['city'] == '' else status[0]['city']['title']
        except KeyError:
            city = 'нет информации'
        try:
            home_town = 'нет информации' if status[0]['home_town'] == '' else status[0]['home_town']
        except KeyError:
            home_town = 'нет информции'
        try:
            university = 'нет информации' if status[0]['university_name'] == '' else status[0]['university_name']
        except KeyError:
            university = 'нет информации'
        try:
            faculty = 'нет информации' if status[0]['faculty_name'] == '' else status[0]['faculty_name']
        except KeyError:
            faculty = 'нет информации'
        try:
            graduation = 'нет информации' if status[0]['graduation'] == 0 else status[0]['graduation']
        except KeyError:
            graduation = 'нет информации'
        education_form = 'нет информации' if 'education_form' not in status[0] else status[0]['education_form']
        education_status = 'нет информации' if 'education_status' not in status[0] else status[0]['education_status']
        followers_count = 'нет информации' if 'followers_count' not in status[0] else status[0]['followers_count']
        try:
            crop_photo = 'нет информации' if status[0]['crop_photo'] == '' else \
            status[0]['crop_photo']['photo']['sizes'][-1]['url']
        except KeyError:
            crop_photo = 'нет фото профиля'
        try:
            activities = 'нет информации' if status[0]['activities'] == '' else status[0]['activities']
        except KeyError:
            activities = 'нет информации'
        try:
            interests = 'нет информации' if status[0]['interests'] == '' else status[0]['interests']
        except KeyError:
            interests = 'нет информации'
        try:
            books = 'нет информации' if status[0]['books'] == '' else status[0]['books']
        except KeyError:
            books = 'нет информации'
        try:
            games = 'нет информации' if status[0]['games'] == '' else status[0]['games']
        except KeyError:
            games = 'нет информации'
        try:
            movies = 'нет информации' if status[0]['movies'] == '' else status[0]['movies']
        except KeyError:
            movies = 'нет информации'
        try:
            music = 'нет информации' if status[0]['music'] == '' else status[0]['music']
        except KeyError:
            music = 'нет информации'
        try:
            quotes = 'нет информации' if status[0]['quotes'] == '' else status[0]['quotes']
        except KeyError:
            quotes = 'нет информации'
        verified = 'Страница верифицирована' if status[0].get('verified') == '1' else 'Страница не верифицирована'
        albums = status[0]['counters'].get('albums', 'нет информации')
        audios = status[0]['counters'].get('audios', 'нет информации')
        friends = status[0]['counters'].get('friends', 'нет информации')
        gifts = status[0]['counters'].get('gifts', 'нет информации')
        groups = status[0]['counters'].get('groups', 'нет информации')
        photos = status[0]['counters'].get('photos', 'нет информации')
        subscriptions_on_profiles = status[0]['counters'].get('subscriptions', 'нет информации')
        videos = status[0]['counters'].get('videos', 'нет информации')
        length_posts = status[0]['counters'].get('posts', 'нет информации')
        try:
            inspired_by = status[0]['personal'].get('inspired_by', 'нет информации')
        except KeyError:
            inspired_by = 'нет информации'
        try:
            langs = ', '.join(status[0]['personal'].get('langs', ['нет информации']))
        except KeyError:
            langs = 'нет информации'
        try:
            religion = status[0]['personal'].get('religion', 'нет информации')
        except KeyError:
            religion = 'нет информации'
        if 'schools' not in status[0]:
            schools = 'нет информации\n'
        else:
            schools = ''
            for school in range(len(status[0]['schools'])):
                schools += f"{status[0]['schools'][school]['name']}\n"

        print(f"Пользователь {self.username}:\n"
              f"id: {user_id}\n"
              f"Аккаунт пользователя {is_account_closed}\n"
              f"Имя: {first_name}\n"
              f"Фамилия: {last_name}\n"
              f"Дата рождения: {bdate}\n"
              f"Статус: {status_text}\n"
              f"Страна: {country}\n"
              f"Город: {city}\n"
              f"Родной город: {home_town}\n"
              f"Школа: {schools}"
              f"Высшее образование: {university}, Факультет: {faculty}, Год окончания: {graduation}, "
              f"Форма обучения: {education_form}, Статус: {education_status}\n"
              f"Языки: {langs}\n"
              f"Количество друзей: {friends}\n"
              f"Количество подписчиков: {followers_count}\n"
              f"Фото профиля: {crop_photo}\n"
              f"Количество альбомов: {albums}\n"
              f"Количество аудио: {audios}\n"
              f"Количество подарков: {gifts}\n"
              f"Количество групп: {groups}\n"
              f"Количество фото в профиле: {photos}\n"
              f"Количество подписок на других пользователей: {subscriptions_on_profiles}\n"
              f"Количество видео: {videos}\n"
              f"Количество постов: {length_posts}\n"
              f"Деятельность: {activities}\n"
              f"Интересы: {interests}\n"
              f"Религия: {religion}\n"
              f"Любимые книги: {books}\n"
              f"Любимые игры: {games}\n"
              f"Любимые фильмы: {movies}\n"
              f"Любимая музыка: {music}\n"
              f"Любимые цитаты: {quotes}\n"
              f"Вдохновляет: {inspired_by}\n"
              f"{verified}\n")

        conn = sqlite3.connect('vk_data.db')
        c = conn.cursor()

        #Создаем таблицу, если она не существует
        c.execute('''CREATE TABLE IF NOT EXISTS user_info
                                          (id INTEGER, is_closed TEXT, first_name TEXT, last_name TEXT, birthday TEXT, status TEXT,
                                          country TEXT, city TEXT, home_town TEXT, university TEXT, faculty TEXT, graduation TEXT,
                                          education_form TEXT, education_status TEXT, number_of_subscribers TEXT,
                                          photo TEXT, activities TEXT, interests TEXT, books TEXT, games TEXT, movies TEXT, music TEXT,
                                          quotes TEXT, verified TEXT, albums TEXT, audios TEXT, friends TEXT, gifts TEXT,
                                          groups TEXT, photos TEXT, subscriptions_on_profiles TEXT, videos TEXT, length_posts TEXT,
                                          inspired_by TEXT, langs TEXT, religion TEXT)''')

        data = c.execute("SELECT id FROM user_info WHERE id = ?", (user_id, )).fetchone()
        if data == None:
            c.execute("INSERT INTO user_info (id, is_closed, first_name, last_name, birthday, status,"
                      "country, city, home_town, university,"
                      "faculty, graduation, education_form, education_status, number_of_subscribers,"
                      "photo, activities, interests, books, games, movies, music,"
                      "quotes, verified, albums, audios, friends, gifts, groups, photos, "
                      "subscriptions_on_profiles, videos, length_posts, inspired_by, "
                      "langs, religion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                      "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (user_id, is_account_closed, first_name, last_name, bdate, status_text, country, city, home_town,
                 university, faculty, graduation, education_form, education_status, followers_count, crop_photo,
                 activities, interests, books, games, movies, music, quotes, verified, albums, audios, friends, gifts, groups, photos,
                 subscriptions_on_profiles, videos, length_posts, inspired_by, langs, religion))
        else:
            c.execute("UPDATE user_info SET is_closed = ?, first_name = ?, last_name = ?, birthday = ?, status = ?, country = ?, city = ?, "
                "home_town = ?, university = ?, faculty = ?, graduation = ?, education_form = ?, education_status = ?, "
                "number_of_subscribers = ?, photo = ?, activities = ?, interests = ?, books = ?, games = ?, movies = ?, "
                "music = ?, quotes = ?, verified = ?, albums = ?, audios = ?, friends = ?, gifts = ?, groups = ?, photos = ?, "
                "subscriptions_on_profiles = ?, videos = ?, length_posts = ?, inspired_by = ?, langs = ?, religion = ? WHERE id = ?",
                (is_account_closed, first_name, last_name, bdate, status_text, country, city, home_town,
                 university, faculty, graduation, education_form, education_status, followers_count, crop_photo,
                 activities, interests, books, games, movies, music, quotes, verified, albums, audios, friends, gifts, groups, photos,
                 subscriptions_on_profiles, videos, length_posts, inspired_by, langs, religion, user_id))

        conn.commit()
        conn.close()

        return status

    def post(self):
        if self.first_name == 'DELETED':
            return f"Аккаунт пользователя был удален"

        try:
            posts = self.session.method("wall.get", {"domain": self.username})
            print(f"Количество постов на аккаунте: {posts['count']}")
            posts = posts['items']
        except vk_api.exceptions.ApiError:
            posts = 'Аккаунт пользователя закрыт'

        print(posts)
        return posts

    def friends(self):
        if self.first_name == 'DELETED':
            return f"Аккаунт пользователя был удален"

        user_id = int(self.session.method("utils.resolveScreenName", {"screen_name": self.username})["object_id"])
        try:
            friends = self.session.method("friends.get", {"user_id": user_id, "fields": "nickname, photo_max_orig"})['items']
        except vk_api.exceptions.ApiError:
            friends = 'Аккаунт пользователя закрыт'

        return friends

    def followers(self):
        if self.first_name == 'DELETED':
            return f"Аккаунт пользователя был удален"

        user_id = int(self.session.method("utils.resolveScreenName", {"screen_name": self.username})["object_id"])
        try:
            followers = self.session.method("users.getFollowers", {"user_id": user_id, "fields": "nickname, photo_max_orig"})["items"]
        except vk_api.exceptions.ApiError:
            followers = 'Аккаунт пользователя закрыт'

        return followers

    def subscriptions(self):
        if self.first_name == 'DELETED':
            return f"Аккаунт пользователя был удален"

        user_id = int(self.session.method("utils.resolveScreenName", {"screen_name": self.username})["object_id"])
        try:
            subscriptions = self.session.method("users.getSubscriptions", {"user_id": user_id, "extended": 1})['items']
        except vk_api.exceptions.ApiError:
            subscriptions = 'Аккаунт пользователя закрыт'

        return subscriptions

    def comments(self):
        if self.first_name == 'DELETED':
            return f"Аккаунт пользователя был удален"

        user_id = int(self.session.method("utils.resolveScreenName", {"screen_name": self.username})["object_id"])
        try:
            posts = self.session.method("wall.get", {"domain": self.username})
            comments = []
            for post in posts['items']:
                try:
                    comment = self.session.method("wall.getComments", {"owner_id": user_id, "post_id": post['id']})['items']
                    if comment:
                        for com in comment:
                            if com['from_id'] == user_id:
                                translator = Translator()
                                text = com['text']
                                translation = translator.translate(text, dest='en')
                                comments.append(translation.text)
                except vk_api.exceptions.ApiError:
                    comments = 'Комментарии закрыты'
        except vk_api.exceptions.ApiError:
            comments = 'Аккаунт пользователя закрыт'

        print(comments)
        return comments

    def last_seen(self):
        if self.first_name == 'DELETED':
            return f"Аккаунт пользователя был удален"

        user_id = int(self.session.method("utils.resolveScreenName", {"screen_name": self.username})["object_id"])
        try:
            last_seen = self.session.method("users.get", {"user_ids": user_id, "fields": "last_seen"})[0]['last_seen']['time']
            converted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_seen))
        except KeyError:
            converted_time = 'Нет информации о последнем посещении'

        print(converted_time)
        return converted_time