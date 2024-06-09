from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, DictProperty
import player

main_player = player.Player()

class MainWindow(Screen):

    def change_button_image(self, button, normal, down):
        button.background_normal = normal
        button.background_down = down
        if button.name == 'new_game':
            self.manager.current = 'GameWindow'

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
        main_player.name = text_name.text
        main_player.gender = gender_spinner.text
        main_player.age = text_age.text
        main_player.profile = profile_spinner.text
        main_player.difficult = difficulty_spinner.text
        main_player.name_brigade = text_name_brigade.text
        main_player.write_json()
        self.manager.current = 'MainGameWindow'

class MainGameWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass



kv = Builder.load_file('interface.kv')

class MyApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    MyApp().run()
