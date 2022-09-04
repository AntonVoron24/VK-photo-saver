import requests
import os
from dotenv import load_dotenv
import datetime as dt
import time
from tqdm import tqdm


load_dotenv()


class VKauth:
    def token(self=None):
        scopes = ['friends', 'photos', 'groups']
        params = {
            'client_id': '51412271',
            'redirect_uri': 'https://oauth.vk.com/blank.html',
            'response_type': 'token',
            'scopes': scopes,
            'v': 5.131
        }

        url = 'https://oauth.vk.com/authorize?'
        resp = requests.get(url, params=params)
        print('Перейди по ссылке ниже')
        print(resp.url)
        print('ВНИМАНИЕ!!!')
        print('Токен никуда не сохраняется и не записывается. После выхода из программы необходимо вновь ввести токен')
        access_token = input('Скопируй из адрессной строки access token и вставь:')
        os.environ['vk_token'] = access_token
        print('Токен получен')
        print('Токен действует пока не выйдем из программы')
        return os.environ['vk_token']


class VKmethods:

    url = 'https://api.vk.com/method/'

    def __init__(self, token):
        self.token = token

    def get_photo(self, id, count=5):
        """ Метод возвращает список словарей из параметров фото аватарок пользователя. По умолчанию 5 последних"""

        params = {
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'owner_id': id,
            'rev': 1,
            'count': count,
            'v': 5.131
        }
        photo_url = self.url + 'photos.get?'
        get_users = requests.get(photo_url, params={**params, 'access_token': self.token}).json()
        photos = []
        likes = []
        today = dt.date.today().strftime('%d.%m.%Y')

        if 'error' in list(get_users):
            print(f"ERROR: {get_users['error']['error_msg']}")
            return photos
        else:
            print('Выгружаем фото из ВК')
            for i in tqdm(get_users['response']['items']):

                if i['likes']['count'] not in likes:
                    photos.append(
                        {
                            'file_name': f"{i['likes']['count']}.jpeg",
                            'size': i['sizes'][-1]['type'],
                            'link': i['sizes'][-1]['url']
                         }
                    )
                else:
                    photos.append(
                        {
                            'file_name': f"{i['likes']['count']} {today} .jpeg",
                            'size': i['sizes'][-1]['type'],
                            'link': i['sizes'][-1]['url']
                        }
                    )
                likes.append(i['likes']['count'])
            return photos

# TODO: Дописать функцию получения фото всех своих друзей. Эта функция должна
#  возвращать словарь по структуре
#  {ID: photos: [{
#           file_name: "",
#           size: "",
#           link: "",
#           }]
#  }



# TODO: ДОПИСАТЬ функцию которая в цикле по ИД пользователя будет сохранять
#  параметры фото в файл JSON с помощью функции save.save_file(photos, user_id)

# TODO: Дописать функцию получения из других альбомов ВК фото и по аналогии сохранить их в файл и на Я.Диск.
#  Нужно выводить список альбомов и предлагать пользователю выбирать альбомы
