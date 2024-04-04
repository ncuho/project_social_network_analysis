import requests

access_token = '7bca63947bca63947bca6394b878ddb93577bca7bca63941dc7bb2a3ca0ffa3fb51e373'

user_id = input("Введите имя пользователя: ")

url_account_info = "https://api.vk.com/method/users.get"
params = {
    'user_ids': user_id,
    'fields': 'bdate, city, country, sex',
    'access_token': access_token,
    'v': '5.130'
}

response = requests.get(url_account_info, params=params)
user_data = response.json()

if user_data['response'][0]['is_closed'] == False:
    url_1 = f"https://api.vk.com/method/wall.get?domain={user_id}&count=2&access_token={access_token}&v=5.130"
    req = requests.get(url_1)
    print(req.text)
else:
    print("Извините, аккаунт пользователя закрыт, поэтому мы можем вывести только основную информацию о странице")
    print(user_data)