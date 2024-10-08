import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

class UserProfile(BoxLayout):
    def __init__(self, user_data, **kwargs):
        super(UserProfile, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Load and display profile picture
        profile_picture_path = user_data.get("profile picture", "")
        if os.path.exists(profile_picture_path):
            self.add_widget(Image(source=profile_picture_path, size_hint=(1, 0.5)))
        else:
            # Display a placeholder if image not found
            self.add_widget(Label(text="No Image Available", size_hint=(1, 0.5)))

        # Display user information
        self.add_widget(Label(text=f"Name: {user_data.get('name', 'N/A')}", size_hint=(1, None), height=30))
        self.add_widget(Label(text=f"Age: {user_data.get('age', 'N/A')}", size_hint=(1, None), height=30))
        self.add_widget(Label(text=f"Gender: {user_data.get('gender', 'N/A')}", size_hint=(1, None), height=30))
        self.add_widget(Label(text=f"Email: {user_data.get('email', 'N/A')}", size_hint=(1, None), height=30))
        self.add_widget(Label(text=f"Phone Number: {user_data.get('phone number', 'N/A')}", size_hint=(1, None), height=30))

class UserProfileApp(App):
    def build(self):
        self.title = "User Profile Viewer"

        # Load user data from JSON file
        try:
            with open("userProfileData_storage.json", "r") as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = []
            print("userProfileData_storage.json file not found.")
        except json.JSONDecodeError:
            self.users = []
            print("Error decoding JSON.")

        # Main layout
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Search bar layout
        search_layout = BoxLayout(size_hint=(1, None), height=40, spacing=10)

        self.search_input = TextInput(
            hint_text="Enter User ID",
            multiline=False,
            size_hint=(0.7, 1)
        )
        search_button = Button(text="Search", size_hint=(0.15, 1))
        search_button.bind(on_press=self.perform_search)

        show_all_button = Button(text="Show All", size_hint=(0.15, 1))
        show_all_button.bind(on_press=self.show_all_profiles)

        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_button)
        search_layout.add_widget(show_all_button)

        self.main_layout.add_widget(search_layout)

        # Container for profiles
        self.profile_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.profile_container.bind(minimum_height=self.profile_container.setter('height'))

        # ScrollView to hold profiles
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.scroll_view.add_widget(self.profile_container)

        self.main_layout.add_widget(self.scroll_view)

        # Initially display all profiles
        self.display_all_profiles()

        return self.main_layout

    def display_all_profiles(self):
        # Clear existing profiles
        self.profile_container.clear_widgets()

        if not self.users:
            self.profile_container.add_widget(Label(text="No user data available.", size_hint=(1, None), height=40))
            return

        for user in self.users:
            user_profile = UserProfile(user_data=user, size_hint_y=None, height=300)
            self.profile_container.add_widget(user_profile)

    def perform_search(self, instance):
        search_id = self.search_input.text.strip()
        if not search_id:
            self.display_message("Please enter a User ID to search.")
            return

        # Find user by userid
        user = next((u for u in self.users if u.get("userid") == search_id), None)

        # Clear existing profiles
        self.profile_container.clear_widgets()

        if user:
            user_profile = UserProfile(user_data=user, size_hint_y=None, height=300)
            self.profile_container.add_widget(user_profile)
        else:
            self.display_message(f"No user found with User ID: {search_id}")

    def show_all_profiles(self, instance):
        self.search_input.text = ""
        self.display_all_profiles()

    def display_message(self, message):
        self.profile_container.clear_widgets()
        self.profile_container.add_widget(Label(text=message, size_hint=(1, None), height=40))

if __name__ == "__main__":
    UserProfileApp().run()