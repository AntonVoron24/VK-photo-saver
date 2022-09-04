import os
import json


def save_file(photos_list, user_id):
    """Функция принимает в себя словарь и ID пользователя в контакте.Cохраняет значения из словаря в файл JSON.
    Также функция сравнивает все значения из уже созданного файла и добавляет элементы,
    которых не было в файле, перезапысывая файл
    """

    links_list = []
    if not photos_list:  # Проверяем есть ли фото
        print('Фото не найдено. Сохранять нечего')
    else:
        web_link = []
        for img in photos_list:
            web_link.append(img['link'])
        if os.path.isfile(f"id{user_id}.json"):  # Проверяем существует ли такой файл и открываем
            with open(f"id{user_id}.json", encoding='utf-8') as f:
                try:
                    file = json.load(f)
                    for param in file['photos']:  # Лобавляем ссылки на фото в список
                        links_list.append(param['link'])
                    for photo in photos_list:  # Проверяем по ссылкам существует ли такое фото
                        if photo['link'] not in links_list:  # Если не существует добавляем
                            file['photos'].append(photo)
                    if web_link != links_list:  # Перезаписываем файл уже с новыми значениями
                        with open(f"id{user_id}.json", 'w', encoding='utf-8') as f_update:
                            json.dump(file, f_update, ensure_ascii=False, indent=2)
                            print('Результат обработки файла:')
                            print('Файл обновлен')
                            print()
                            return
                    else:
                        print('В файле уже есть все фото')

                except json.decoder.JSONDecodeError:  # Если ловим ошибку то пересоздаем файл с новыми значениями
                    with open(f"id{user_id}.json", 'w', encoding='utf-8') as f_new:
                        json.dump({'photos': photos_list}, f_new, ensure_ascii=False, indent=2)
                        print('Добавлено')
                        return

        else:
            with open(f"id{user_id}.json", 'w', encoding='utf-8') as f:
                json.dump({'photos': photos_list}, f, ensure_ascii=False, indent=2)
                print('Добавлено')
    return
