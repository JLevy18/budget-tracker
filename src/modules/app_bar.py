from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from src.modules.drop_down import DynamicDropDown, import_action, export_action, about_action
import os
import sys

file_menu_items = [
    {"text": "Import", "action": import_action},
    {"text": "Export", "action": export_action},
    {"is_separator": True},  # Separator
    {"text": "Settings", "action": None},
    {"text": "Check for updates", "action": None},
]

help_menu_items = [
    {"text": "About", "action": about_action},
]

class AppBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create dropdowns
        self.file_dropdown = DynamicDropDown(menu_items=file_menu_items)
        self.help_dropdown = DynamicDropDown(menu_items=help_menu_items)
