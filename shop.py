import random
import json
import os

PATH = 'data/shop/'


class ButtonShop:
    def __init__(self, **kwargs):
        # Базовые атрибуты с дефолтными значениями
        self.name = kwargs.get('name', '')
        self.difficult = kwargs.get('difficult', '')
        self.profile = kwargs.get('profile', '')
        self.post = kwargs.get('post', '')
        self.cost = int(kwargs.get('cost', 0))
        self.background_normal = kwargs.get('background_normal', '')
        self.background_down = kwargs.get('background_down', '')
        self.img_animation = kwargs.get('img_animation', '')

        # Список "issue" — если его нет, создаём пустой список
        self.issue = kwargs.get('issue', [])


class Shop():
    def __init__(self):
        self.page = 0
        self.list_button = {}
        self.screen_btn = ''

    def create_shop(self):
        files = os.listdir(PATH)
        if len(files) != 0:
            for i in files:
                file = os.path.join(PATH, i)
                file_name = os.path.basename(file)
                basename = os.path.splitext(file_name)
                #basename[0] - имя файла
                with open(file, 'r', encoding='utf-8') as db_file:
                    data = json.load(db_file)
                    list_btn =[]
                    for i in data:
                        button_shop = ButtonShop()
                        button_shop.name = i
                        for j in data[i]:
                            if j == 'Сложности':
                                button_shop.difficult = data[i][j]
                            elif j == 'Принадлежность':
                                button_shop.profile = data[i][j]
                            elif j == 'Должность':
                                button_shop.post = data[i][j]
                            elif j == 'Стоимость':
                                button_shop.cost = data[i][j]
                            elif j == 'Анимация':
                                button_shop.img_animation = data[i][j]
                            elif j.startswith('Исход'):
                                button_shop.issue.append(data[i][j])
                            elif j.startswith('КартинкаНормальная'):
                                button_shop.background_normal = data[i][j]
                            elif j.startswith('КартинкаНажата'):
                                button_shop.background_down = data[i][j]
                        list_btn.append(button_shop)
                    self.list_button[basename[0]] = list_btn


