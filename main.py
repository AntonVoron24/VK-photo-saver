import save
from save import *
from VK import *
import yadisk
from pprint import pprint

"""Для выполнения скрипта можно вставить токен доступа в файл .env"""


def vk_token():
    """ Функция проверяет наличие токен в файле .env
    Возвращает валидный токен или прерывает выполнение"""

    if os.getenv('vk_token'):
        vk_token = os.getenv('vk_token')
        print(os.getenv('vk_token'))
    else:
        vk_token = VKauth.token()
        print(os.getenv('vk_token'))
    return vk_token


if os.getenv('ya_token'):
    ya = yadisk.YaDisk(token=os.getenv('ya_token'))
    if ya.check_token():
        print('Токен действителен')
    else:
        print('Неверный токен Я.Диск. Проверь корректность токена')
        print('Ссылка на Яндекс полигон')
        print('https://yandex.ru/dev/disk/poligon/')
        ya = input('Введи токен полученный с Яндекс полигона: ')
else:
    print('Ссылка на Яндекс полигон')
    print('https://yandex.ru/dev/disk/poligon/')
    ya_token = input('Введи токен полученный с Яндекс полигона: ')
    ya = yadisk.YaDisk(token=ya_token)
    if ya.check_token():
        print('Токен действителен')


method = VKmethods(vk_token())
user_id = input('Введите ID пользователя: ')
count = input('Введите какое количество фото хотите сохранить (по умолчанию 5): ')
if count:
    photos = method.get_photo(user_id, count=count)
else:
    photos = method.get_photo(user_id)
# photos это список словарей с параметрами фоток аватарок пользователей


save.save_file(photos, user_id)  # Сохраняем найденные фото в файл

if not ya.is_dir(f'id{user_id}'):  # Проверяем есть ли папка для сохранения по ИД пользователя
    print('Сохраняем фото на Я.Диск')
    ya.mkdir(f'id{user_id}')
    for photo in tqdm(photos):
        ya.upload_url(photo['link'], f'id{user_id}/{photo["file_name"]}')  # Загружаем фото
        # TODO: Вставить ссылку на папку Я.Диск с загруженными фото
else:
    pass
# TODO: Дописать чтоб открывалась папка Я.Диск, сравнивались названия фото и добавлялись те, которых еще нет


# TODO: Написать консольный вобор команд
# TODO: В самом конце обработать все пустые вводы, неверные токены и т.д.
