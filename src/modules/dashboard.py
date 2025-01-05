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
from ctypes import windll, Structure, c_int, byref

# Register the class with Kivy
import os
import sys


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if getattr(sys, "frozen", False):  # If running in a PyInstaller bundle
    base_path = sys._MEIPASS
    KV_DIR = os.path.join(sys._MEIPASS, "ui")
else:
    base_path = os.path.abspath(".")  # Current working directory in dev mode
    KV_DIR = os.path.join(BASE_DIR, "ui")

font_path = os.path.join(base_path, "resources", "MaterialRounded.ttf")
logo = os.path.join(base_path, "resources", "BudgetTracker.png")

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'dpi', 'auto')
Config.set('kivy', 'window', 'sdl2')
Config.set("kivy", "default_font", font_path)

Builder.load_file(os.path.join(KV_DIR, "dashboard.kv"))

Factory.register("HoverableButton", cls=HoverableButton)

class MARGINS(Structure):
    _fields_ = [("cxLeftWidth", c_int),
                ("cxRightWidth", c_int),
                ("cyTopHeight", c_int),
                ("cyBottomHeight", c_int)]

def enable_shadow(hwnd):
    margins = MARGINS(-1, -1, -1, -1)  # Extend the shadow into the entire window area
    windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, byref(margins))

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
        self.font_path = font_path
        self.logo = logo

    def build(self):

        Window.clearcolor = self.hex_to_rgba("#14202E")
        Window.borderless = True
        Window.custom_titlebar = True
        Window.set_custom_titlebar(TitleBar())
        Window.set_icon(os.path.join(os.path.dirname(__file__), "../resources/BudgetTracker.ico"))

        hwnd = windll.user32.GetForegroundWindow()
        enable_shadow(hwnd)

        return DashboardScreen(self.budget)

    def minimize_window(self):
        Window.minimize()

    def maximize_window(self):
        if self.window_state["is_maximized"]:
            # Restore the original size and position
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
            self.window_state["is_maximized"] = False
        else:
            # Save the current size and position
            self.window_state["size"] = Window.size[:]
            self.window_state["pos"] = (Window.left, Window.top)

            # Maximize the window
            from ctypes import windll
            hwnd = windll.user32.GetForegroundWindow()
            user32 = windll.user32
            user32.SetProcessDPIAware()  # Enable DPI awareness
            screen_width = user32.GetSystemMetrics(0)  # Full screen width
            screen_height = user32.GetSystemMetrics(1)  # Full screen height
            # Explicitly resize and position the window
            windll.user32.MoveWindow(hwnd, 0, 0, screen_width, screen_height, True)
            self.window_state["is_maximized"] = True


    def close_window(self):
        self.stop()

    @staticmethod
    def hex_to_rgba(hex_color):
        hex_color = hex_color.lstrip("#")
        return [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)] + [1]