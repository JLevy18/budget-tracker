from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from src.modules.hover_behavior import HoverableButton

def import_action():
    print("Import selected")

def export_action():
    print("Export selected")

def about_action():
    print("About selected")

def contact_support_action():
    print("Contact Support selected")


class DynamicDropDown(DropDown):
    def __init__(self, menu_items, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.auto_width = False
        
        with self.canvas.before:
            Color(rgba=self.app.hex_to_rgba("#2B4257"))  # Background color
            self.background_rect = Rectangle(size=self.size, pos=self.pos)

        # Bind the dropdown size and position to the background rectangle
        self.bind(size=self._update_background, pos=self._update_background)

        self._button_width = 150  # Default button width
        self._button_height = 20  # Default button height
        self._font_size = 14  # Smaller font size for dropdown options
        
        for item in menu_items:
            if item.get("is_separator", False):
                self.add_widget(self._create_separator())
            else:
                button = self._create_menu_button(item["text"], item["action"])
                self.add_widget(button)
                print(f"Added button to dropdown: {button}, type: {type(button)}")
                
        # Adjust the dropdown size based on the number of children
        self._adjust_dropdown_size()

    def _update_background(self, *args):
        """Update the background rectangle and shadow."""
        # Update background
        self.background_rect.size = self.size
        self.background_rect.pos = self.pos

    def _adjust_dropdown_size(self):
        """Adjust the size of the dropdown to fit its content."""
        total_height = sum(
            (child.height) for child in self.children
        )
        self.size = (self._button_width, total_height)
        self._update_background()

    def _create_menu_button(self, text, action):
        button = HoverableButton(
            text=text,
            align_text_left=True,
            size_hint=(None, None),
            size=(self._button_width, self._button_height),
            font_size=self._font_size,  # Smaller font size
            on_release=lambda *args: (action() if action else None, self.dismiss()),
        )
        print(f"Created button: {button}, type: {type(button)}")
        return button

    def _create_separator(self):
        separator = Label(size_hint_y=None, height=1)
        with separator.canvas.before:
            color = Color(rgba=self.app.hex_to_rgba("#88A9C3"))
            rect = Rectangle(size=separator.size, pos=separator.pos)

        # Bind the separator's size and position to the rectangle
        def update_rectangle(instance, value):
            rect.size = instance.size
            rect.pos = instance.pos

        separator.bind(size=update_rectangle, pos=update_rectangle)
        return separator