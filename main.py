from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image


class OpenScreenManager(Screen):
    pass

class ImageButton(ButtonBehavior, Image):
    pass

class HomeScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        #layout = GridLayout(cols=2)
        #layout.add_widget(Label())#(text='User Name'))
        self.username = TextInput(multiline=False)
        #layout.add_widget(self.username)
        #layout.add_widget(Label())#(text='Password'))
        self.password = TextInput(password=True, multiline=False)
        #layout.add_widget(self.password)
        #self.add_widget(layout)

class RegisterScreen(Screen):
    pass

GUI = Builder.load_file("main.kv")

class MyApp(App):

    def build(self):
        return GUI#LoginScreen()

    def change_screen(self, screen_name):
        # Get Screen_manager from kv file
        # Get the existing ScreenManager
        screen_manager = self.root.ids["screen_manager"]
        
        # Set the desired transition
        screen_manager.transition = WipeTransition()
        
        # Change the current screen
        screen_manager.current = screen_name

if __name__ == '__main__':
    MyApp().run()