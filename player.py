import random
import json
import os

PATH = 'data/main_data.json'

class Player():
    def __init__(self, name='', gender='', age='', profile='', difficult='', name_brigade=''):
        self.name = name
        self.gender = gender
        self.age = age
        self.profile = profile
        self.difficult = difficult
        self.name_brigade = name_brigade
        self.health = 100
        self.hunger = 100
        self.mood = 100
        self.money = 50
        self.special_money = 0
        self.post = 'Кандидат'
        self.popularity = 1

    def write_json(self):
        dict_player = {
            'name':self.name,
            'gender': self.gender,
            'age': self.age,
            'profile': self.profile,
            'difficult': self.difficult,
            'name_brigade': self.name_brigade,
            'health': self.health,
            'hunger': self.hunger,
            'mood': self.mood,
            'money': self.money,
            'special_money': self.special_money,
            'post': self.post,
            'popularity': self.popularity}

        if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
            with open(PATH, 'w', encoding='utf-8') as db_file:
                json.dump(dict_player, db_file, ensure_ascii=False)
            # Перезаписать файл
        else:
            with open(PATH, 'w', encoding='utf-8') as db_file:
                json.dump(dict_player, db_file, ensure_ascii=False)



