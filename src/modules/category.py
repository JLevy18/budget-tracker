from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class Category(BoxLayout):
    name = StringProperty("Category Name")  # Default text for category name
    def __init__(self, **kwargs):
        super().__init__(orientation="horizontal", **kwargs)

