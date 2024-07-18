import random

from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, DictProperty
from kivy.animation import Animation
from kivy.clock import Clock
from functools import partial
import player
import shop

main_player = player.Player()
main_player.read_json()

main_shop = shop.Shop()
main_shop.create_shop()


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
            self.show_warning('Заполните все поля')

    def show_warning(self, text_warning):
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


class MainGameWindow(Screen):

    def update_data(self, rect_back):
        self.ids['text_health'].text = str(main_player.health)
        self.ids['text_hunger'].text = str(main_player.hunger)
        self.ids['text_money'].text = str(main_player.money)
        self.ids['text_mood'].text = str(main_player.mood)
        self.ids['text_populyarity'].text = str(main_player.popularity)
        self.ids['text_supermoney'].text = str(main_player.special_money)
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
        self.update_data(False)

class ShopGameWindow(Screen):

    def back(self):
        self.manager.current = 'MainGameWindow'

    def change_screen(self, dt):
        global main_shop
        list_button = []
        for button in main_shop.list_button:
            probability = []
            for element in button.issue:
                a = element['Вреоятность']
                while a > 0:
                    probability.append(element['Вреоятность'])
                    a -= 1

            btn = {'text': '',
                   'player_image': self.ids['player_image'],
                   'screen': self,
                   'issue': button.issue,
                   'background_normal': button.background_normal,
                   'background_down': button.background_down,
                   'probability': probability}
            list_button.append(btn)
        self.ids['listButtonView'].data = list_button

    def update_data(self, rect_back):
        Clock.schedule_once(self.change_screen)
        self.ids['text_health'].text = str(main_player.health)
        self.ids['text_hunger'].text = str(main_player.hunger)
        self.ids['text_money'].text = str(main_player.money)
        self.ids['text_mood'].text = str(main_player.mood)
        self.ids['text_populyarity'].text = str(main_player.popularity)
        self.ids['text_supermoney'].text = str(main_player.special_money)
        if rect_back != False:
            c_g = rect_back.get_group('rect_back')
            if main_player.current_time_of_day == 'day':
                c_g[0].size = (0, 0)
            else:
                c_g[0].size = self.size
        main_player.write_json()

class CustomButton(Button):
    def on_release(self, *args, **kwargs):
        self.player_image.source = 'Images/gif/actions/PlayerPlusMoney.zip'
        self.player_image.anim_delay = 0.04
        self.player_image.reload()
        number = random.choice(self.probability)
        issue = ''
        text_message = ''
        for element in self.issue:
            if element['Вреоятность'] == number:
                issue = element
                text_message = element['Текст']
                break
        if issue['Оповещение']:
            self.show_warning(text_message)
        self.changes(issue, self.screen)
        self.screen.update_data(False)

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

    def show_warning(self, text_warning):
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



class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('interface.kv')


class MyApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MyApp().run()
