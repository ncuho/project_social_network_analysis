import sqlite3
import vk_api


class User_pars:
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
        return status[0]

    def friends(self):
        user_id = int(self.session.method("utils.resolveScreenName", {"screen_name": self.username})["object_id"])
        friends = self.session.method("friends.get", {"user_id": user_id, "fields": "nickname, photo_max_orig"})[
            'items']
        rez = []
        for i in friends:
            rez.append(f"{i['id']}) {i['first_name']} {i['last_name']}")

        return rez

    def get_friends_id(self):
        user_id = int(self.session.method("utils.resolveScreenName", {"screen_name": self.username})["object_id"])
        friends = self.session.method("friends.get", {"user_id": user_id, "fields": "nickname, photo_max_orig"})[
            'items']
        rez = []
        for i in friends:
            rez.append(i['id'])
        return rez

    def followers(self):
        user_id = int(self.session.method("utils.resolveScreenName", {"screen_name": self.username})["object_id"])
        followers = \
            self.session.method("users.getFollowers", {"user_id": user_id, "fields": "nickname, photo_max_orig"})[
                "items"]

        return followers

    def comments(self):
        user_id = int(self.session.method("utils.resolveScreenName", {"screen_name": self.username})["object_id"])
        try:
            posts = self.session.method("wall.get", {"domain": self.username})
            comments = []
            for post in posts['items']:
                try:
                    comment = self.session.method("wall.getComments", {"owner_id": user_id, "post_id": post['id']})[
                        'items']
                    if comment:
                        for com in comment:
                            if com['from_id'] == user_id:
                                comments.append(com['text'])
                except vk_api.exceptions.ApiError:
                    comments = 'Комментарии закрыты'
        except vk_api.exceptions.ApiError:
            comments = 'Аккаунт пользователя закрыт'

        return comments

    def subscriptions(self):
        user_id = int(self.session.method("utils.resolveScreenName", {"screen_name": self.username})["object_id"])
        subscriptions = self.session.method("users.getSubscriptions", {"user_id": user_id, "extended": 1})['items']

        return subscriptions

# https://vk.com/id306744629
# https://vk.com/vladlolka_chuvstv
# https://vk.com/id4236944
# https://vk.com/dgorbunov
# https://vk.com/abalakireva2011
