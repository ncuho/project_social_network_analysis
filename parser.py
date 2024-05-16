import sqlite3
import vk_api


class User:
    def __init__(self, username):
        self.username = username
        self.access_token = 'vk1.a.ae4PjjbPvm8L5vXH1F-26IEjvSsn8cUbexDNV6QtQ_qjePgHiPN3HNU_UdA_oBU9xSNhA9EWPwLk7gCDvk9g7ydePZHnAJ0Ih_j2TRUY8sLWOQztj3nc_fPyL5DW6Ut3-H4Nv34zvKLu6S4mH57yJAzbdNmFrIP5PK41sebbFP1pB75RaK_y1OvbhbCS7Awe-clGfajGGpziOLNbDSeAug'
        self.session = vk_api.VkApi(token=self.access_token)
        self.vk = self.session.get_api()

    def main_info(self):
        fields = "activities,about,counters,books,bdate,can_be_invited_group,connections,contacts,city,country,crop_photo,domain,education,exports,followers_count,friend_status,has_photo,has_mobile,home_town,photo_100,photo_200,photo_200_orig,photo_400_orig,photo_50,sex,site,schools,screen_name,status,verified,games,interests,is_favorite,is_friend,is_hidden_from_feed,last_seen,maiden_name,military,movies,music,nickname,occupation,online,personal,photo_id,photo_max,photo_max_orig,quotes,relation,relatives,timezone,tv,universities"
        status = self.session.method("users.get", {"user_id": self.username, "fields": fields})
        if "error" in status:
            print("Ошибка при запросе к API VK")
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
        subscriptions_on_profiles = 'нет информации' if 'subscriptions' not in status[0]['counters'] else status[0]['counters']['subscriptions']
        videos = 'нет информации' if 'videos' not in status[0]['counters'] else status[0]['counters']['videos']
        length_posts = 'нет информации' if 'posts' not in status[0]['counters'] else status[0]['counters']['posts']
        inspired_by = 'нет информации' if 'inspired_by' not in status[0]['personal'] else status[0]['personal']['inspired_by']
        langs = 'нет информации' if 'langs' not in status[0]['personal'] else ', '.join(status[0]['personal']['langs'])
        religion = 'нет информации' if 'religion' not in status[0]['personal'] else status[0]['personal']['religion']
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
        posts = self.session.method("wall.get", {"domain": self.username})

        close = User.main_info(self)
        is_closed = close[0]["is_closed"]

        if is_closed == True:
            return print("Аккаунт закрыт")

        print(f"Количество постов на аккаунте: {posts['count']}")
        posts = posts['items']

        return posts

    def friends(self):
        user_id = int(self.session.method("utils.resolveScreenName", {"screen_name": self.username})["object_id"])
        friends = self.session.method("friends.get", {"user_id": user_id, "fields": "nickname, photo_max_orig"})['items']

        return friends

    def followers(self):
        user_id = int(self.session.method("utils.resolveScreenName", {"screen_name": self.username})["object_id"])
        followers = self.session.method("users.getFollowers", {"user_id": user_id, "fields": "nickname, photo_max_orig"})["items"]

        return followers

    def subscriptions(self):
        user_id = int(self.session.method("utils.resolveScreenName", {"screen_name": self.username})["object_id"])
        subscriptions = self.session.method("users.getSubscriptions", {"user_id": user_id, "extended": 1})['items']

        return subscriptions



#https://vk.com/id306744629
#https://vk.com/vladlolka_chuvstv
#ncuhh
#https://vk.com/id4236944
#https://vk.com/dgorbunov
newUser = User("vladlolka_chuvstv")
newUser.main_info()
newUser.subscriptions()
newUser.post()