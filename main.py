from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen

class HomeScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

#Enter Username and password
class PasswordScreen(GridLayout):

    def __init__(self, **kwargs):
        super(PasswordScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

GUI = Builder.load_file("main.kv")

class MyApp(App):

    def build(self):
        return GUI#LoginScreen()

    def change_screen(self, screen_name):
        # Get Screen_manager from kv file
        #print(self.root.ids)
        screen_manager = self.root.ids["screen_manager"]
        screen_manager.current = screen_name

if __name__ == '__main__':
    MyApp().run()