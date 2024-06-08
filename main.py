from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, DictProperty


class MainWindow(Screen):

    def change_button_image(self, button, normal, down):
        button.background_normal = normal
        button.background_down = down
        if button.name == 'new_game':
            self.manager.current = 'GameWindow'

class GameWindow(Screen):

    options = DictProperty(
        {"Easy": "Images/buttons/backToMainMenu/button_press.png", "Medium": "Images/buttons/backToMainMenu/button_press.png", "HARD": "Images/buttons/backToMainMenu/button_press.png"}
    )

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('interface.kv')

class MyApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    MyApp().run()
