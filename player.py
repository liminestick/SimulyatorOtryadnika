import random
import json
import os

new_game_data = 'data/game_data/new_game_data.json'
current_player_json = 'data/game_data/current_player.json'

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
        self.new_game = True

    def new_game_write_json(self):
        dict_player = {
            'name': self.name,
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
            'popularity': self.popularity,
            'new_game': False}

        with open(current_player_json, 'w', encoding='utf-8') as db_file:
            json.dump(dict_player, db_file, ensure_ascii=False)

    def read_json(self):
        if os.path.isfile(current_player_json) and os.access(current_player_json, os.R_OK):
            with open(current_player_json, 'r', encoding='utf-8') as db_file:
                self.read_file(db_file)
        else:
            with open(new_game_data, 'r', encoding='utf-8') as db_file:
                self.read_file(db_file)

    def read_file(self, db_file):
        data = json.load(db_file)
        self.name = data['name']
        self.gender = data['gender']
        self.age = data['age']
        self.profile = data['profile']
        self.difficult = data['difficult']
        self.name_brigade = data['name_brigade']
        self.health = data['health']
        self.hunger = data['hunger']
        self.mood = data['mood']
        self.money = data['money']
        self.special_money = data['special_money']
        self.post = data['post']
        self.popularity = data['popularity']
        self.new_game = data['new_game']
