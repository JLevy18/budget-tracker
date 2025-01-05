from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.utils import platform
from src.modules.titlebar import TitleBar
from src.modules.hover_behavior import HoverableButton

# Register the class with Kivy
import os
import sys

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'resizable', True)
Config.set('kivy', 'window', 'sdl2')
Config.set('graphics', 'dpi', 'auto')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Move up one level to 'src'

if getattr(sys, "frozen", False):  # If running in a PyInstaller bundle
    KV_DIR = os.path.join(sys._MEIPASS, "src", "ui")
else:
    KV_DIR = os.path.join(BASE_DIR, "ui")  # Resolve to 'src/ui'

Builder.load_file(os.path.join(KV_DIR, "dashboard.kv"))

Factory.register("HoverableButton", cls=HoverableButton)

class DashboardScreen(BoxLayout):
    def __init__(self, budget, **kwargs):
        super().__init__(**kwargs)
        self.budget = budget
        self.display_budget()

    def display_budget(self):
        # Access the GridLayout with the ID "budget_info"
        budget_tab = self.ids["budget_info"]
        for _, row in self.budget.budget_df.iterrows():
            budget_tab.add_widget(Label(text=row["Category"]))
            budget_tab.add_widget(Label(text=row["Name"]))
            budget_tab.add_widget(Label(text=str(row["Cost per Month"])))


class BudgetTrackerApp(App):
    """
    The Kivy App class that launches the Dashboard.
    """
    def __init__(self, budget, **kwargs):
        super().__init__(**kwargs)
        self.budget = budget
        self.window_state = {
            "size": Window.size,
            "pos": (Window.left, Window.top),
            "is_maximized": False
        }

    def build(self):

        Window.clearcolor = self.hex_to_rgba("#14202E")
        Window.borderless = True
        Window.custom_titlebar = True
        Window.set_custom_titlebar(TitleBar())
        Window.set_icon(os.path.join(os.path.dirname(__file__), "../resources/BudgetTracker.ico"))

        return DashboardScreen(self.budget)

    def minimize_window(self):
        Window.minimize()

    def maximize_window(self):
        if self.window_state["is_maximized"]:
            # Restore the original size and position
            if platform == "win":
                from ctypes import windll
                hwnd = windll.user32.GetForegroundWindow()  # Get current window handle
                user32 = windll.user32
                # Restore size and position using MoveWindow
                user32.MoveWindow(
                    hwnd,
                    int(self.window_state["pos"][0]),  # Restore X position
                    int(self.window_state["pos"][1]),  # Restore Y position
                    int(self.window_state["size"][0]),  # Restore width
                    int(self.window_state["size"][1]),  # Restore height
                    True,
                )
            else:
                Window.borderless = True
                Window.size = self.window_state["size"]
                Window.left, Window.top = self.window_state["pos"]

            self.window_state["is_maximized"] = False
        else:
            # Save the current size and position
            self.window_state["size"] = Window.size[:]
            self.window_state["pos"] = (Window.left, Window.top)

            # Platform-specific logic for screen size
            if platform == "win":
                from ctypes import windll
                hwnd = windll.user32.GetForegroundWindow()
                user32 = windll.user32
                user32.SetProcessDPIAware()  # Enable DPI awareness
                screen_width = user32.GetSystemMetrics(0)  # Full screen width
                screen_height = user32.GetSystemMetrics(1)  # Full screen height
                # Explicitly resize and position the window
                windll.user32.MoveWindow(hwnd, 0, 0, screen_width, screen_height, True)
            else:
                # Maximize on Linux/MacOS
                screen_width, screen_height = Window.system_size
                Window.size = (screen_width, screen_height)
                Window.left, Window.top = 0, 0

            self.window_state["is_maximized"] = True


    def close_window(self):
        self.stop()

    @staticmethod
    def hex_to_rgba(hex_color):
        hex_color = hex_color.lstrip("#")
        return [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)] + [1]