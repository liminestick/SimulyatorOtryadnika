import json
import random

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import DictProperty
from kivy.clock import Clock
from functools import partial
import player
import shop

#При запускае игры читаем данные игрока и создаем объект под данным из файла
main_player = player.Player()
main_player.read_json()

#При запуске игры собираем магазин и создаем объект магазина
main_shop = shop.Shop()
main_shop.create_shop()

def read_modife():
    path_to_mod = "data/game_data/modifier_item.json"
    with open(path_to_mod, 'r', encoding='utf-8') as file:
        modife = json.load(file)

    return modife

dict_mod = read_modife()

class MainWindow(Screen):

    def change_button_image(self, button):
        if button.name == 'new_game':
            if main_player.new_game:
                self.manager.current = 'GameWindow'
            else:
                self.show_question()
        if button.name == 'continue_game':
            self.manager.current = 'MainGameWindow'

    def show_question(self):
        btn_yes = Button(text='', size_hint_y=0.3,
                         background_normal='Images/answers/yes/button_normal.png',
                         background_down='Images/answers/yes/button_press.png')
        btn_no = Button(text='', size_hint_y=0.3,
                        background_normal='Images/answers/no/button_normal.png',
                        background_down='Images/answers/no/button_press.png')
        bx_v = BoxLayout(orientation='vertical')
        bx_h = BoxLayout(orientation='horizontal')
        popup = Popup(title='', separator_color=(1, 1, 1, 0),
                      size_hint=(0.7, 0.5),
                      background='Images/popup/popup_normal.png',
                      auto_dismiss=False)
        lb = Label(text="У вас уже есть сохраненая игра. Хотите начать новую игру?",
                   text_size=(700, None),
                   halign='center',
                   font_name='fonts/EpilepsySansBold.ttf',
                   font_size=60)
        bx_v.add_widget(lb)
        bx_v.add_widget(bx_h)
        bx_h.add_widget(btn_yes)
        bx_h.add_widget(btn_no)
        popup.add_widget(bx_v)
        btn_yes.bind(on_press=partial(self.start_game, element=popup))
        btn_no.bind(on_press=popup.dismiss)
        popup.open()

    def start_game(self, *args, **kwargs):
        kwargs['element'].dismiss()
        self.manager.current = 'GameWindow'


class GameWindow(Screen):
    Screen.list_dict = {"Легко": "Images/difficult/easy.png",
                        "Нормально": "Images/difficult/medium.png",
                        "Сложно": "Images/difficult/hard.png",
                        "ССО": "Images/profile/SSO.png",
                        "СПО": "Images/profile/SPO.png",
                        "СОП": "Images/profile/SOP.png",
                        "Мужской": "Images/gender/male.png",
                        "Женский": "Images/gender/female.png"}
    options = DictProperty(Screen.list_dict)

    def changing_picture(self, spinner):
        if spinner.text != '':
            spinner.background_normal = Screen.list_dict[spinner.text]
            spinner.text = ''

    def start_new_game(self, text_name, gender_spinner, text_age, profile_spinner, difficulty_spinner,
                       text_name_brigade):
        global main_player
        main_player = player.Player()
        play_game = True
        if text_name.text != '':
            main_player.name = text_name.text
        else:
            play_game = False

        if gender_spinner.state_image != 'Images/gender/normal.png':
            main_player.gender = gender_spinner.text
        else:
            play_game = False

        if text_age.text != '':
            main_player.age = text_age.text
        else:
            play_game = False

        if profile_spinner.state_image != 'Images/profile/normal.png':
            main_player.profile = profile_spinner.text
        else:
            play_game = False

        if difficulty_spinner.state_image != 'Images/difficult/normal.png':
            main_player.difficult = difficulty_spinner.text
        else:
            play_game = False

        if text_name_brigade.text != '':
            main_player.name_brigade = text_name_brigade.text
        else:
            play_game = False

        if play_game:
            main_player.new_game_write_json()
            self.manager.current = 'MainGameWindow'
        else:
            show_warning('Заполните все поля')


class MainGameWindow(Screen):

    def update_data(self, rect_back):
        update_basic_attributes(self)
        self.ids['text_post'].text = "Должность: " + str(main_player.post)
        self.ids['text_days_lived'].text = "Дней прожито: " + str(int(main_player.days_lived))
        if rect_back != False:
            c_g = rect_back.get_group('rect_back')
            if main_player.current_time_of_day == 'day':
                c_g[0].size = (0, 0)
            else:
                c_g[0].size = self.size
        main_player.write_json()

    def shop_screen(self):
        self.manager.current = 'ShopGameWindow'

        # Код чтобы скрывать и добавлять кнопки
        # btn_1 = Button(text='Кнопка')
        # btn_work.opacity = 0
        # btn_work.size_hint_y = 0.0
        # button_collection.add_widget(btn_1)

    def add_button2(self):
        pass

    def change_day(self, rect_back):
        main_player.days_lived += 0.5
        c_g = rect_back.get_group('rect_back')
        if main_player.current_time_of_day == 'day':
            main_player.current_time_of_day = 'night'
            c_g[0].size = self.size
        else:
            main_player.current_time_of_day = 'day'
            c_g[0].size = (0, 0)
            check_player(main_player)
        self.update_data(False)


class ShopGameWindow(Screen):

    def back(self):
        self.manager.current = 'MainGameWindow'

    def change_screen(self, dt):
        global main_shop
        list_button = {}

        for i in main_shop.list_button:
            list_btn = []
            for button in main_shop.list_button[i]:
                probability = []
                for element in button.issue:
                    a = element['Вероятность']
                    while a > 0:
                        probability.append(element['Вероятность'])
                        a -= 1

                btn = {'text': '',
                       'player_image': self.ids['player_image'],
                       'screen': self,
                       'img_animation': button.img_animation,
                       'issue': button.issue,
                       'probability': probability}
                if button.background_normal != '':
                    btn['background_normal'] = button.background_normal
                    btn['background_down'] = button.background_down
                else:
                    btn['text'] = button.name

                list_btn.append(btn)
            list_button[i] = list_btn
        main_shop.screen_btn = list_button
        self.ids['listButtonView'].data = main_shop.screen_btn['product']

    def update_data(self, rect_back):
        self.update_text()
        Clock.schedule_once(self.change_screen)
        if rect_back != False:
            c_g = rect_back.get_group('rect_back')
            if main_player.current_time_of_day == 'day':
                c_g[0].size = (0, 0)
            else:
                c_g[0].size = self.size
        main_player.write_json()

    def update_text(self):
        update_basic_attributes(self)

    def changing_section(self, name_shop):
        global main_shop
        self.ids['listButtonView'].data = main_shop.screen_btn[name_shop]


class CustomButton(Button):
    def on_release(self, *args, **kwargs):
        if self.img_animation != '':
            self.player_image.source = self.img_animation
        else:
            self.player_image.source = 'Images/player/normal/normal.png'
        self.player_image.anim_delay = 0.07
        self.player_image.reload()
        number = random.choice(self.probability)
        issue = ''
        text_message = ''
        for element in self.issue:
            if element['Вероятность'] == number:
                issue = element
                text_message = element['Текст']
                break
        if issue.get('Оповещение', False):
            show_warning(issue['Оповещение'])
        if issue.get('Модификатор'):
            modifier = issue['Модификатор']
            add_modifier(main_player, modifier)
        self.changes(issue, self.screen)
        self.screen.update_text()

    def changes(self, issue, screen):
        for i in issue['Изменения']:
            if i == 'Голод':
                main_player.hunger = main_player.hunger + int(issue['Изменения']['Голод'])
            elif i == 'Настроение':
                main_player.mood = main_player.mood + int(issue['Изменения']['Настроение'])
            elif i == 'Здоровье':
                main_player.health = main_player.health + int(issue['Изменения']['Здоровье'])
            elif i == 'Деньги':
                main_player.money = main_player.money + int(issue['Изменения']['Деньги'])
            elif i == 'СуперДеньги':
                main_player.special_money = main_player.special_money + int(issue['Изменения']['СуперДеньги'])
            elif i == 'Популярность':
                main_player.popularity = main_player.popularity + int(issue['Изменения']['Популярность'])


class WindowManager(ScreenManager):
    pass


def show_warning(text_warning):
    btn_close = Button(text='', size_hint_y=0.2,
                       background_normal='Images/answers/clear/button_normal.png',
                       background_down='Images/answers/clear/button_press.png')
    bx = BoxLayout(orientation='vertical')
    popup = Popup(title='', separator_color=(1, 1, 1, 0),
                  size_hint=(0.7, 0.5),
                  background='Images/popup/popup_normal.png',
                  auto_dismiss=False)
    popup.separator_color = (1, 1, 1, 0)
    lb = Label(text=text_warning,
               font_name='fonts/EpilepsySansBold.ttf',
               font_size=60,
               halign='center',
               text_size=(700, None))
    bx.add_widget(lb)
    bx.add_widget(btn_close)
    popup.add_widget(bx)
    btn_close.bind(on_press=popup.dismiss)
    popup.open()

def update_basic_attributes(screen):
    screen.ids['text_health'].text = str(main_player.health)
    screen.ids['text_hunger'].text = str(main_player.hunger)
    screen.ids['text_money'].text = str(main_player.money)
    screen.ids['text_mood'].text = str(main_player.mood)
    screen.ids['text_populyarity'].text = str(main_player.popularity)
    screen.ids['text_supermoney'].text = str(main_player.special_money)

def check_player(main_player):
    check_modifier(main_player)

def check_modifier(main_player):

    if len(main_player.modifier) > 0:
        for modif in main_player.modifier:
            if "Здоровье" in modif:
                main_player.health += + int(modif['Здоровье'])
            if "Настроение" in modif:
                main_player.mood += + int(modif['Настроение'])
            if "Голод" in modif:
                main_player.health += + int(modif['Голод'])
            if "Деньги" in modif:
                main_player.health += + int(modif['Деньги'])
            if "Популярность" in modif:
                main_player.health += + int(modif['Популярность'])

def add_modifier(main_player, modifier):
    pass

kv = Builder.load_file('interface.kv')

class MyApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MyApp().run()
