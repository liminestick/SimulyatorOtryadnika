from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

class MainWindow(Screen):

    def change_button_image(self, button, normal, down):
        button.background_normal = normal
        button.background_down = down

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('interface.kv')

class MyApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    MyApp().run()
