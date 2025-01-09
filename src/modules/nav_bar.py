from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
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
    pass