from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import os

class TestApp(App):
    def build(self):
        # Проверяем, существует ли KV-файл
        kv_path = 'test_interface.kv'
        if not os.path.exists(kv_path):
            print(f"KV-файл '{kv_path}' не найден!")
        else:
            print(f"KV-файл '{kv_path}' найден.")

        # Проверяем, существуют ли изображения
        background_path = 'Images/backgrounds/main_background.png'
        if not os.path.exists(background_path):
            print(f"Файл фона '{background_path}' не найден!")

        return Builder.load_file('test_interface.kv')

if __name__ == '__main__':
    TestApp().run()