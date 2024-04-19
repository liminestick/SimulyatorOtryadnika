from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex

Config.set('graphics', 'width', '540')
Config.set('graphics', 'height', '960')

# Загрузка шрифта
LabelBase.register('MyFont', fn_regular='fonts/EpilepsySansBold.ttf')

class MainWindow(Screen):

    def change_button_image(self, button, normal, down):
        button.background_normal = normal
        button.background_down = down
        self.manager.current = 'GameWindow'


class GameWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('interface.kv')

class MyApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    MyApp().run()
