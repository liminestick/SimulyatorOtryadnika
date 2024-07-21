import random
import json
import os

PATH = 'data/shop/'


class ButtonShop():
    def __init__(self, name='', difficult='', profile='', post='', cost=0, background_normal='', background_down='', img_animation=''):
        self.name = name
        self.difficult = difficult
        self.profile = profile
        self.post = post
        self.img_animation = img_animation
        self.background_normal = background_normal
        self.background_down = background_down
        self.issue = []


class Shop():
    def __init__(self):
        self.page = 0
        self.list_button = []

    def create_shop(self):
        if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
            with open(PATH, 'r', encoding='utf-8') as db_file:
                data = json.load(db_file)
                for i in data:
                    button_shop = ButtonShop()
                    button_shop.name = i
                    for j in data[i]:
                        if j == 'Сложности':
                            button_shop.difficult = data[i][j]
                        elif j == 'Принадлежность':
                            button_shop.profile = data[i][j]
                        elif j == 'Должность':
                            button_shop.profile = data[i][j]
                        elif j == 'Стоимость':
                            button_shop.profile = data[i][j]
                        elif j == 'Анимация':
                            button_shop.img_animation = data[i][j]
                        elif j.startswith('Исход'):
                            button_shop.issue.append(data[i][j])
                        elif j.startswith('КартинкаНормальная'):
                            button_shop.background_normal = data[i][j]
                        elif j.startswith('КартинкаНажата'):
                            button_shop.background_down = data[i][j]
                    self.list_button.append(button_shop)
