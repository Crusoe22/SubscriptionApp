#first app
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput 
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout


class childApp(GridLayout):
    def __init__(self, **kwargs):
        super(childApp, self).__init__()
        self.cols = 2 #can change number of columns

        # Array to store student data
        self.userProfile_data = []

        # Widgets for user input 
        self.add_widget(Label(text = 'Profile Name'))
        self.s_name = TextInput()
        self.add_widget(self.s_name)

        #copy to add other widgets
        self.add_widget(Label(text = 'Your age'))
        self.s_age = TextInput(input_filter='int')
        self.add_widget(self.s_age)

        #copy to add other widgets
        self.add_widget(Label(text = 'Your Gender'))
        self.s_gender = TextInput()
        self.add_widget(self.s_gender)

        #copy to add other widgets
        self.add_widget(Label(text = 'Your Email'))
        self.s_email = TextInput()
        self.add_widget(self.s_email)

        #copy to add other widgets
        self.add_widget(Label(text = 'Your Phone Number'))
        self.s_phoneNumber = TextInput(input_filter='int')
        self.add_widget(self.s_phoneNumber)

        #submit/clear button
        self.press = Button(text = 'Click me to submit your profile!')
        self.press.bind(on_press = self.click_me)
        self.add_widget(self.press)

    def click_me(self, instance):
        if not self.s_name.text or not self.s_age.text or not self.s_gender.text or not self.s_email.text or not self.s_phoneNumber.text:
            self.show_popup("Error", "Please fill in all the fields")
        elif "@" not in self.s_email.text or "." not in self.s_email.text:
            self.show_popup("Error", "Please enter a valid email address")
        elif len(self.s_phoneNumber.text) < 10:
            self.show_popup("Error", "Phone number must contain at least 10 digits")

        else:
            # Append user data to the array
            userProfile = {
                "name": self.s_name.text,
                "age": self.s_age.text,
                "gender": self.s_gender.text,
                "email": self.s_email.text,
                "phone number": self.s_phoneNumber.text
            }
            self.userProfile_data.append(userProfile)

            print(f"Added:{userProfile}")
            print(f"All User's Data: {self.userProfile_data}")
            print("")

            # Clear all fields after submission 
            self.s_name.text = ''
            self.s_age.text = ''
            self.s_gender.text = ''
            self.s_email.text = ''
            self.s_phoneNumber.text = ''

            self.show_popup("Sucess", "Profile submitted sucessfully!")
            print("profile added")

    def show_popup(self, title, message):
        # Create a pop up with a message
        layout = BoxLayout(orientation='vertical', padding=10)
        popup_label = Label(text=message)
        close_button = Button(text="Close", size_hint=(1, 0.2))
        layout.add_widget(popup_label)
        layout.add_widget(close_button)
        
        popup_window = Popup(title=title, content=layout, size_hint=(0.6, 0.4))
        close_button.bind(on_press=popup_window.dismiss)
        popup_window.open()
          


class parentApp(App):
    def build(self):
        return childApp()
    
if __name__ == "__main__":
    parentApp().run()