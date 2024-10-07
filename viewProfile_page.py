import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

class UserProfile(BoxLayout):
    def __init__(self, user_data, **kwargs):
        super(UserProfile, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 5
        self.spacing = 5

        # Load and display profile picture
        profile_picture_path = user_data["profile picture"]
        if os.path.exists(profile_picture_path):
            self.add_widget(Image(source=profile_picture_path, size_hint=(1, 0.5)))

        # Display user information
        self.add_widget(Label(text=f"Name: {user_data['name']}", size_hint=(1, None), height=30))
        self.add_widget(Label(text=f"Age: {user_data['age']}", size_hint=(1, None), height=30))
        self.add_widget(Label(text=f"Gender: {user_data['gender']}", size_hint=(1, None), height=30))
        self.add_widget(Label(text=f"Email: {user_data['email']}", size_hint=(1, None), height=30))
        self.add_widget(Label(text=f"Phone Number: {user_data['phone number']}", size_hint=(1, None), height=30))

class UserProfileApp(App):
    def build(self):
        # Load user data from JSON file
        with open("userProfileData_storage.json", "r") as f:
            users = json.load(f)

        layout = BoxLayout(orientation='vertical', padding=5, spacing=5)

        # Create a ScrollView to contain user profiles
        scroll_view = ScrollView(size_hint=(1, 1))
        profile_container = BoxLayout(orientation='vertical', size_hint_y=None)
        profile_container.bind(minimum_height=profile_container.setter('height'))

        for user in users:
            user_profile = UserProfile(user_data=user, size_hint_y=None, height=300)
            profile_container.add_widget(user_profile)

        scroll_view.add_widget(profile_container)
        layout.add_widget(scroll_view)

        return layout

if __name__ == "__main__":
    UserProfileApp().run()