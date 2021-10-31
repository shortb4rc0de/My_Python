import vk_api
import threading
import json
import emoji
import csv
from config import token
import time


class Parser:

    def __init__(self, user_id, session):
        """
            :param user_id: int -> id vk user
            :param session: object vk api -> connection session vk
        """
        try:
            self.user_id = int(user_id)
        except:
            print("That's not an int!")
        self.session = session

        self.lst = ['bdate', 'sex', 'relation', 'occupation', 'interests',
                    'activities', 'personal', 'about', 'music',
                    'movies', 'tv', 'military', 'books']  # Массив с интересующими нас данными
        self.dict = []
        self.data = []
        self.dict_info = {}

        self.mas = ['bdate', 'sex', 'relation', 'name', 'type', 'langs', 'alcohol', 'smoking', 'inspired_by',
                    'life_main', 'people_main', 'religion', 'political', 'interests', 'activities', 'about',
                    'music', 'movies', 'tv', 'military', 'books']

    def id_groups(self):
        """
            :return: list[int] -> group list of user vk
        """
        session = self.session
        try:
            groups = session.method("groups.get", {"user_id": self.user_id})['items']
        except:
            return ['']
        return groups

    def status_group(self, group_id):
        """
            :param: int -> group id
            :return: str ->  status group
        """
        session = self.session
        try:
            status_groups = session.method("status.get", {"group_id": group_id})['text']
            if ":" in emoji.demojize(status_groups):  # check on smile
                return ''
            try:
                # check on coding 'cp1251', because error could be when write this data to csv
                status_groups.encode('cp1251')
                return status_groups
            except:
                return ''
        except:
            return ''

    def titles_video(self):
        """
            :return: list[string] -> list of video name
        """
        titles_video = []
        session = self.session
        try:
            videos = session.method("video.get", {"owner_id": self.user_id})['items']
        except:
            return ['']
        titles_video_symbols = [item for item in [videos[x]['title'] for x in range(len(videos))] if
                                ":" not in emoji.demojize(item)]  # check on smile
        for i in range(len(titles_video_symbols)):
            try:
                # check on coding 'cp1251', because error could be when write this data to csv
                titles_video_symbols[i].encode('cp1251')
                titles_video.append(titles_video_symbols[i])
            except:
                continue
        return titles_video

    def into_dict(self, user):

        for item in self.lst:  # Получаем нужные нам данные со страницы пользователя
            self.data += self.session.method('users.get', {'user_id': user, 'fields': [item]})

        num = 0  # Счётчик, для элементов в массиве (каждый элемент является словарём)
        for elem in self.data:  # Записываем эти данные в отдельный словарь
            for key in elem:
                if key in self.lst:
                    try:
                        self.dict.append(self.data[num][key])
                    except KeyError:
                        continue
                    num += 1
        for key, value in zip(self.lst, self.dict):
            self.dict_info[key] = value

        return self.dict_info

    def unpack(self):  # Распаковываем элементы в словаре, которые сами являются словарём
        mas = {}
        info = ['military', 'occupation', 'personal']
        for key in self.dict_info:
            if key in info:
                for key_2 in self.dict_info[key]:
                    try:
                        mas[key_2] = self.dict_info[key][key_2]
                    except:
                        print('не прочитать')

        for elem in self.dict_info:
            if type(self.dict_info[elem]) != dict:
                mas[elem] = self.dict_info[elem]

        return mas

    def decoder(self, mas):  # Декодируем информацию о поле, отношениях и тд, тк она идём в цифрах
        for key in mas:
            if type(mas[key]) == int:
                match key:
                    case 'sex':
                        match mas[key]:
                            case 0:
                                mas[key] = 'не указано'
                            case 1:
                                mas[key] = 'женский'
                            case 2:
                                mas[key] = 'мужской'
                    case 'relation':
                        match mas[key]:
                            case 0:
                                mas[key] = 'не указано'
                            case 1:
                                mas[key] = 'не женат/не замужем'
                            case 2:
                                mas[key] = 'есть друг/есть подруга'
                            case 3:
                                mas[key] = 'помолвлен/помолвлена'
                            case 4:
                                mas[key] = 'женат/замужем'
                            case 5:
                                mas[key] = 'всё сложно'
                            case 6:
                                mas[key] = 'в активном поиске'
                            case 7:
                                mas[key] = 'влюблён/влюблена'
                            case 8:
                                mas[key] = 'в гражданском браке'
                    case 'political':
                        match mas[key]:
                            case 0:
                                mas[key] = 'не указано'
                            case 1:
                                mas[key] = 'коммунистические'
                            case 2:
                                mas[key] = 'социалистические'
                            case 3:
                                mas[key] = 'умеренные'
                            case 4:
                                mas[key] = 'либеральные'
                            case 5:
                                mas[key] = 'консервативные'
                            case 6:
                                mas[key] = 'монархические'
                            case 7:
                                mas[key] = 'ультраконсервативные'
                            case 8:
                                mas[key] = 'индифферентные'
                            case 9:
                                mas[key] = 'либертарианские'
                    case 'people_main':
                        match mas[key]:
                            case 0:
                                mas[key] = 'не указано'
                            case 1:
                                mas[key] = 'ум и креативность'
                            case 2:
                                mas[key] = 'доброта и честность'
                            case 3:
                                mas[key] = 'красота и здоровье'
                            case 4:
                                mas[key] = 'власть и богатство'
                            case 5:
                                mas[key] = 'смелость и упорство'
                            case 6:
                                mas[key] = 'юмор и жизнелюбие'
                    case 'life_main':
                        match mas[key]:
                            case 0:
                                mas[key] = 'не указано'
                            case 1:
                                mas[key] = 'семья и дети'
                            case 2:
                                mas[key] = 'карьера и деньги'
                            case 3:
                                mas[key] = 'развлечения и отдых'
                            case 4:
                                mas[key] = 'наука и исследования'
                            case 5:
                                mas[key] = 'совершенствование мира'
                            case 6:
                                mas[key] = 'саморазвитие'
                            case 7:
                                mas[key] = 'красота и искусство'
                            case 8:
                                mas[key] = 'слава и влияние'
                    case 'smoking':
                        match mas[key]:
                            case 0:
                                mas[key] = 'не указано'
                            case 1:
                                mas[key] = 'резко негативное'
                            case 2:
                                mas[key] = 'негативное'
                            case 3:
                                mas[key] = 'компромиссное'
                            case 4:
                                mas[key] = 'нейтральное'
                            case 5:
                                mas[key] = 'положительное'
                    case 'alcohol':
                        match mas[key]:
                            case 0:
                                mas[key] = 'не указано'
                            case 1:
                                mas[key] = 'резко негативное'
                            case 2:
                                mas[key] = 'негативное'
                            case 3:
                                mas[key] = 'компромиссное'
                            case 4:
                                mas[key] = 'нейтральное'
                            case 5:
                                mas[key] = 'положительное'

        return mas

    def dict_sort(self, dictionary):
        dct = {}
        for param in self.mas:
            for key in dictionary:
                if key == param:
                    dct[param] = dictionary[key]
                    break
        return dct

    def into_csv(self, dictionary, group_video):


        to_file = [dictionary[key] for key in dictionary]

        if len(to_file) < len(self.mas):
            while len(to_file) < len(self.mas):
                to_file.append('None')

        for i in range(len(to_file)):
            try:
                to_file[i].encode('cp1251')
                if to_file[i] == '' or to_file[i] == []:
                    to_file[i] = 'None'
            except:
                to_file[i] = 'None'
        to_file += list(group_video.values())

        with open('database.csv', 'a', encoding='cp1251', newline='') as file:
            writer1 = csv.writer(file, delimiter=';')
            writer1.writerow(to_file)

        file.close()


if __name__ == '__main__':

    session = vk_api.VkApi(token=token)
    vk = session.get_api()

    with open('jsonUsers.json') as f:  # Распаковываем файл с id пользовтелей
        file_with_ids = json.load(f)

    with open('database.csv', 'w', encoding='cp1251', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['bdate', 'sex', 'relation', 'name', 'type', 'langs', 'alcohol', 'smoking', 'inspired_by',
                         'life_main', 'people_main', 'religion', 'political', 'interests', 'activities', 'about',
                         'music', 'movies', 'tv', 'military', 'books', 'title_group', 'video_name'])
    csv_file.close()

    mas_id = []

    for elem in file_with_ids['id']:
        mas_id.append(int(elem))

    mas_id_set = set(mas_id)

    for ids in mas_id_set:
        s_time = time.time()
        start = Parser(ids, session)
        groups_id = start.id_groups()  # get groups id
        statuses_group = [start.status_group(group_id) for group_id in groups_id[0:3]]  # get group statuses
        titles_videos = start.titles_video()   # get video titles
        start.into_dict(ids)
        start.into_csv(start.dict_sort(start.decoder(start.unpack())), {'title_group': statuses_group, 'video_name': titles_videos})
        print(ids, f'{time.time() - s_time} seconds')

