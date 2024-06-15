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
import player

main_player = player.Player()
main_player.read_json()

class MainWindow(Screen):

    def change_button_image(self, button, normal, down):
        button.background_normal = normal
        button.background_down = down
        if button.name == 'new_game':
            self.manager.current = 'GameWindow'
        if button.name == 'continue_game':
            self.manager.current = 'MainGameWindow'


class GameWindow(Screen):

    Screen.list_dict = {"Легко": "Images/difficult/easy.png",
               "Нормально": "Images/difficult/medium.png",
               "Сложно": "Images/difficult/hard.png",
               "ССО": "Images/profile/SSO.png",
               "СПО": "Images/profile/SPO.png",
               "СОП": "Images/profile/SOP.png",
               "Мужской":"Images/gender/male.png",
               "Женский":"Images/gender/female.png"}
    options = DictProperty(Screen.list_dict)

    def changing_picture(self, spinner):
        if spinner.text != '':
            spinner.background_normal = Screen.list_dict[spinner.text]
            spinner.text = ''

    def start_new_game(self, text_name, gender_spinner, text_age, profile_spinner, difficulty_spinner, text_name_brigade):
        global main_player
        main_player = player.Player()
        main_player.name = text_name.text
        main_player.gender = gender_spinner.text
        main_player.age = text_age.text
        main_player.profile = profile_spinner.text
        main_player.difficult = difficulty_spinner.text
        main_player.name_brigade = text_name_brigade.text
        main_player.write_json()
        self.manager.current = 'MainGameWindow'

class MainGameWindow(Screen):

    def fill_data(self, text_health, text_hunger, text_money, text_mood, text_populyarity, text_supermoney, text_post):
        text_health.text = str(main_player.health)
        text_hunger.text = str(main_player.hunger)
        text_money.text = str(main_player.money)
        text_mood.text = str(main_player.mood)
        text_populyarity.text = str(main_player.popularity)
        text_supermoney.text = str(main_player.special_money)
        text_post.text = text_post.text + str(main_player.post)

    def shop_screen(self):
        self.manager.current = 'ShopGameWindow'


        # Код чтобы скрывать и добавлять кнопки
        # btn_1 = Button(text='Кнопка')
        # btn_work.opacity = 0
        # btn_work.size_hint_y = 0.0
        # button_collection.add_widget(btn_1)

    def add_button2(self):
        btn_close = Button(text='Понял принял')
        bx = BoxLayout(orientation='vertical')
        popup = Popup(size_hint=(None, None), size=(400, 400),
                      background='Images/buttons/profile/button_normal.png',
                      auto_dismiss=False)
        lb = Label(text='Привет отрядник')
        bx.add_widget(lb)
        bx.add_widget(btn_close)
        popup.add_widget(bx)
        btn_close.bind(on_press=popup.dismiss)
        popup.open()

class ShopGameWindow(Screen):

    def work1(self, player_image):
        player_image.source = 'Images/gif/actions/PlayerPlusMoney.gif'



class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('interface.kv')

class MyApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    MyApp().run()
