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
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import DictProperty

# Optional: Set a background color for the window
Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Light grey background

class UserProfile(BoxLayout):
    user_data = DictProperty()

    def __init__(self, user_data, **kwargs):
        super(UserProfile, self).__init__(**kwargs)
        self.user_data = user_data
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 150
        self.padding = 10
        self.spacing = 20

        # Add a background with rounded corners
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.bg = RoundedRectangle(radius=[10, 10, 10, 10], pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        # Profile Picture
        profile_picture_path = user_data.get("profile picture", "")
        if os.path.exists(profile_picture_path):
            profile_img = Image(source=profile_picture_path, size_hint=(None, 1), width=120)
        else:
            # Placeholder image
            profile_img = Image(source='placeholder.png', size_hint=(None, 1), width=120)
        self.add_widget(profile_img)

        # User Information Layout
        info_layout = BoxLayout(orientation='vertical', spacing=5)

        # Name Label
        name_label = Label(
            text=f"[b]{user_data.get('name', 'N/A')}[/b]",
            markup=True,
            font_size='18sp',
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30
        )
        info_layout.add_widget(name_label)

        # Age and Gender Layout
        age_gender_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=25)
        age_label = Label(
            text=f"Age: {user_data.get('age', 'N/A')}",
            font_size='14sp',
            color=(0.3, 0.3, 0.3, 1)
        )
        gender_label = Label(
            text=f"Gender: {user_data.get('gender', 'N/A')}",
            font_size='14sp',
            color=(0.3, 0.3, 0.3, 1)
        )
        age_gender_layout.add_widget(age_label)
        age_gender_layout.add_widget(gender_label)
        info_layout.add_widget(age_gender_layout)

        # Email and Phone Layout
        contact_layout = BoxLayout(orientation='vertical', spacing=2, size_hint_y=None, height=50)
        email_label = Label(
            text=f"📧 {user_data.get('email', 'N/A')}",
            font_size='14sp',
            color=(0.3, 0.3, 0.3, 1),
            halign="left",
            valign="middle"
        )
        email_label.bind(size=email_label.setter('text_size'))
        phone_label = Label(
            text=f"📞 {user_data.get('phone number', 'N/A')}",
            font_size='14sp',
            color=(0.3, 0.3, 0.3, 1),
            halign="left",
            valign="middle"
        )
        phone_label.bind(size=phone_label.setter('text_size'))
        contact_layout.add_widget(email_label)
        contact_layout.add_widget(phone_label)
        info_layout.add_widget(contact_layout)

        self.add_widget(info_layout)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

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
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Search bar layout
        search_layout = BoxLayout(size_hint=(1, None), height=50, spacing=10)

        self.search_input = TextInput(
            hint_text="Enter User ID",
            multiline=False,
            size_hint=(0.7, 1),
            background_normal='',
            background_color=(1, 1, 1, 1),
            padding=[10, 10]
        )
        search_button = Button(
            text="Search",
            size_hint=(0.15, 1),
            background_normal='',
            background_color=(0.2, 0.6, 0.86, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        search_button.bind(on_press=self.perform_search)

        show_all_button = Button(
            text="Show All",
            size_hint=(0.15, 1),
            background_normal='',
            background_color=(0.6, 0.6, 0.6, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        show_all_button.bind(on_press=self.show_all_profiles)

        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_button)
        search_layout.add_widget(show_all_button)

        self.main_layout.add_widget(search_layout)

        # Container for profiles
        self.profile_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
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
            self.profile_container.add_widget(
                Label(
                    text="No user data available.",
                    size_hint=(1, None),
                    height=40,
                    color=(1, 0, 0, 1)
                )
            )
            return

        for user in self.users:
            user_profile = UserProfile(user_data=user)
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
            user_profile = UserProfile(user_data=user)
            self.profile_container.add_widget(user_profile)
        else:
            self.display_message(f"No user found with User ID: {search_id}")

    def show_all_profiles(self, instance):
        self.search_input.text = ""
        self.display_all_profiles()

    def display_message(self, message):
        self.profile_container.clear_widgets()
        self.profile_container.add_widget(
            Label(
                text=message,
                size_hint=(1, None),
                height=40,
                color=(1, 0, 0, 1)
            )
        )

if __name__ == "__main__":
    UserProfileApp().run()