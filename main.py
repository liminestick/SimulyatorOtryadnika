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

    def fill_data(self, text_health, text_hunger, text_money, text_mood, text_populyarity, text_supermoney, text_post):
        text_health.text = str(main_player.health)
        text_hunger.text = str(main_player.hunger)
        text_money.text = str(main_player.money)
        text_mood.text = str(main_player.mood)
        text_populyarity.text = str(main_player.popularity)
        text_supermoney.text = str(main_player.special_money)
        text_post.text = "Должность: " + str(main_player.post)

    def shop_screen(self):
        self.manager.current = 'ShopGameWindow'

        # Код чтобы скрывать и добавлять кнопки
        # btn_1 = Button(text='Кнопка')
        # btn_work.opacity = 0
        # btn_work.size_hint_y = 0.0
        # button_collection.add_widget(btn_1)

    def add_button2(self):
        pass


class ShopGameWindow(Screen):

    def back(self):
        self.manager.current = 'MainGameWindow'

    def on_enter(self, *args):
        Clock.schedule_once(self.change_screen)

    def change_screen(self, dt):
        global main_shop
        list_button = []
        for button in main_shop.list_button:
            btn = {'text': str(button.name), 'player_image': self.ids['player_image']}
            list_button.append(btn)
        self.ids['listButtonView'].data = list_button

class CustomButton(Button):
    def on_release(self):
        self.player_image.source = 'Images/gif/actions/PlayerPlusMoney.zip'
        self.player_image.anim_delay = 0.04
        self.player_image.reload()

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('interface.kv')


class MyApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MyApp().run()
