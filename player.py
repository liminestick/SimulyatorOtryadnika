import random
import json
import os

new_game_data = 'data/game_data/new_game_data.json'
current_player_json = 'data/game_data/current_player.json'

class Player():
    def __init__(self, **kwargs):
        # Установка базовых значений по умолчанию
        self.name = kwargs.get('name', '')
        self.gender = kwargs.get('gender', '')
        self.age = kwargs.get('age', 0)
        self.profile = kwargs.get('profile', '')
        self.difficult = kwargs.get('difficult', '')
        self.name_brigade = kwargs.get('name_brigade', '')
        self.current_time_of_day = kwargs.get('current_time_of_day', 'day')

        # Статы
        self.health = kwargs.get('health', 100)
        self.hunger = kwargs.get('hunger', 20)
        self.mood = kwargs.get('mood', 20)
        self.money = kwargs.get('money', 0)
        self.special_money = kwargs.get('special_money', 0)
        self.days_lived = kwargs.get('days_lived', 0)
        self.post = kwargs.get('post', 'Кандидат')
        self.popularity = kwargs.get('popularity', 1)
        self.modifier = kwargs.get('modifier', [{"Здоровье": "+2", "Настроение": "+2"}])
        self.new_game = kwargs.get('new_game', True)

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
            'days_lived': self.days_lived,
            'current_time_of_day': self.current_time_of_day,
            'special_money': self.special_money,
            'post': self.post,
            'modifier': self.modifier,
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
        self.days_lived = data['days_lived']
        self.current_time_of_day = data['current_time_of_day']
        self.special_money = data['special_money']
        self.post = data['post']
        self.modifier = data['modifier']
        self.popularity = data['popularity']
        self.new_game = data['new_game']

    def write_json(self):
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
            'days_lived': self.days_lived,
            'current_time_of_day': self.current_time_of_day,
            'special_money': self.special_money,
            'post': self.post,
            'modifier': self.modifier,
            'popularity': self.popularity,
            'new_game': False}

        with open(current_player_json, 'w', encoding='utf-8') as db_file:
            json.dump(dict_player, db_file, ensure_ascii=False)
