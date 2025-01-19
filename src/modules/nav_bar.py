from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty
from src.modules.hover_behavior import HoverableButton

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if getattr(sys, "frozen", False):  # If running in a PyInstaller bundle
    # Resolve `src/ui` relative to the PyInstaller bundle
    KV_DIR = os.path.join(sys._MEIPASS, "ui")
else:
    # Resolve `src/ui` relative to the current script's directory
    KV_DIR = os.path.join(BASE_DIR, "ui")

Builder.load_file(os.path.join(KV_DIR, "nav_bar.kv"))

class NavBar(AnchorLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.selected_button = None

    def on_kv_post(self, base_widget):
        """This method is called after the KV language is fully applied."""
        # Set the dashboard button as the default selection
        dashboard_button = self.ids.get("dashboard_button")
        if dashboard_button:
            self.select_button(dashboard_button)
    
    def select_button(self, button):
        # Update font for the previously selected button
        if self.selected_button:
            self.selected_button.font_name = self.app.font_path_extralight

        # Set the new button as selected
        self.selected_button = button
        self.selected_button.font_name = self.app.font_path