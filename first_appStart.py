#first app
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput 
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
import json
import os
import shutil  # To copy the selected image to the desired location

json_file_path = "userProfileData_storage.json"
profile_pics_directory = r"C:\Users\nolan\OneDrive\Documents\ProfilePics_storage_app"  # Folder to store profile pictures

class childApp(GridLayout):
    def __init__(self, **kwargs):
        super(childApp, self).__init__()
        self.cols = 2 #can change number of columns

        # Path to store user profile data
        self.userProfile_data_json = json_file_path

        # Widgets for user input 
        self.add_widget(Label(text = 'Profile Name'))
        self.s_name = TextInput()
        self.add_widget(self.s_name)

        # Widget for age
        self.add_widget(Label(text = 'Your age'))
        self.s_age = TextInput(input_filter='int')
        self.add_widget(self.s_age)

        # Widget for gender
        self.add_widget(Label(text = 'Your Gender'))
        self.s_gender = TextInput()
        self.add_widget(self.s_gender)

        # Widget for email
        self.add_widget(Label(text = 'Your Email'))
        self.s_email = TextInput()
        self.add_widget(self.s_email)

        # Widget for phone number
        self.add_widget(Label(text = 'Your Phone Number'))
        self.s_phoneNumber = TextInput(input_filter='int')
        self.add_widget(self.s_phoneNumber)

        # FileChooser to select profile picture
        self.add_widget(Label(text = 'Select Profile Picture'))
        self.profile_picture_button = Button(text="Choose Image")
        self.profile_picture_button.bind(on_press=self.open_filechooser)
        self.add_widget(self.profile_picture_button)

        # Submit button
        self.press = Button(text = 'Click me to submit your profile!')
        self.press.bind(on_press = self.click_me)
        self.add_widget(self.press)

        # Variable to store the selected profile picture path
        self.selected_image_path = None

    # Open FileChooser for image selection
    def open_filechooser(self, instance):
        filechooser = FileChooserIconView()
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(filechooser)

        select_button = Button(text="Select", size_hint=(1, 0.2))
        popup_content.add_widget(select_button)

        popup_window = Popup(title="Choose Profile Picture", content=popup_content, size_hint=(0.8, 0.8))

        # Bind the select button to save the selected image path and close the popup
        select_button.bind(on_press=lambda x: self.select_image(filechooser, popup_window))
        popup_window.open()

    # Function to select the image
    def select_image(self, filechooser, popup_window):
        if filechooser.selection:
            self.selected_image_path = filechooser.selection[0]  # Get the selected file path
            print(f"Selected image: {self.selected_image_path}")
        popup_window.dismiss()


    # Function to get the next available user ID
    def get_next_userid(self, users):
        if not users:
            return 1  # Start at 1 if there are no users
        user_ids = [int(user["userid"]) for user in users]
        return max(user_ids) + 1  # Increment the highest user ID
    
    # Function to add a new user profile
    def click_me(self, instance):
        if not self.s_name.text or not self.s_age.text or not self.s_gender.text or not self.s_email.text or not self.s_phoneNumber.text:
            self.show_popup("Error", "Please fill in all the fields")
        elif "@" not in self.s_email.text or "." not in self.s_email.text:
            self.show_popup("Error", "Please enter a valid email address")
        elif len(self.s_phoneNumber.text) < 10:
            self.show_popup("Error", "Phone number must contain at least 10 digits")
        else:
            # Read existing profiles from the JSON file, if it exists
            if os.path.exists(self.userProfile_data_json):
                with open(self.userProfile_data_json, 'r') as file:
                    try:
                        profiles = json.load(file)
                        if isinstance(profiles, dict):
                            profiles = [profiles]  # Convert dict to list if needed
                        elif not isinstance(profiles, list):
                            profiles = []  # Start fresh if structure is unexpected
                    except json.JSONDecodeError:
                        profiles = []  # Start fresh if file is corrupted
            else:
                profiles = []  # Start with an empty list if no file exists

            # Step 2: Find the next available user ID
            new_userid = self.get_next_userid(profiles)

            # Copy the selected image to the profile pictures directory
            image_extension = os.path.splitext(self.selected_image_path)[1]
            new_image_filename = f"profile_{new_userid}{image_extension}"
            new_image_path = os.path.join(profile_pics_directory, new_image_filename)
            shutil.copy(self.selected_image_path, new_image_path)  # Copy image to the designated directory

            # Step 3: Create a new user profile with the next available ID
            userProfile = {
                "userid": str(new_userid),  # Assign unique ID
                "name": self.s_name.text,
                "age": self.s_age.text,
                "gender": self.s_gender.text,
                "email": self.s_email.text,
                "phone number": self.s_phoneNumber.text,
                "profile picture": new_image_path  # Save the path to the profile picture
            }

            # Append the new profile to the list
            profiles.append(userProfile)

            # Write the updated list back to the file
            with open(self.userProfile_data_json, 'w') as file:
                json.dump(profiles, file, indent=4)

            # Clear all fields after submission 
            self.s_name.text = ''
            self.s_age.text = ''
            self.s_gender.text = ''
            self.s_email.text = ''
            self.s_phoneNumber.text = ''
            self.selected_image_path = None

            self.show_popup("Success", "Profile submitted successfully!")
            print(f"Added: {userProfile}")

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