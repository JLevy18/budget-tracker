
import os
import sys

from kivy.app import App
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.layout import Layout
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition, FadeTransition
from kivy.graphics import Color, Line

from src.modules.app_bar import AppBar
from src.modules.nav_bar import NavBar
from src.modules.content_area import ContentArea
from src.modules.hover_behavior import HoverableButton
from src.modules.classes.budget import Budget

from ctypes import windll, Structure, c_int, byref

def import_action():
    print("Import selected")

def export_action():
    print("Export selected")

file_menu_items = [
    {"text": "Import", "action": import_action},
    {"text": "Export", "action": export_action},
    {"is_separator": True},  # Separator
    {"text": "Settings", "action": None},
    {"text": "Check for updates", "action": None},
]

# Determine base paths
if getattr(sys, "frozen", False):  # If running in a PyInstaller bundle
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  # Current script's directory

KV_DIR = os.path.join(base_path, "ui")
Builder.load_file(os.path.join(KV_DIR, "budget_tracker.kv"))
Builder.load_file(os.path.join(KV_DIR, "views", "budget_view.kv"))
Builder.load_file(os.path.join(KV_DIR, "views", "dashboard_view.kv"))
Builder.load_file(os.path.join(KV_DIR, "views", "transaction_view.kv"))

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'dpi', 'auto')
Config.set('kivy', 'window', 'sdl2')
Config.set('graphics', 'show_fps', '1')
Config.set('modules', 'monitor', '1')

def initialize_app(base_dir, is_prod):
    """
    Initialize the application by ensuring directories exist and loading the budget.
    """

    return BudgetTrackerApp(is_prod=is_prod)


def print_widget_tree(widget, level=0):
    """
    Recursively print the widget tree for debugging purposes.
    """
    prefix = " " * (level * 2)
    print(f"{prefix}{widget.__class__.__name__}: {widget}")
    if hasattr(widget, 'children') and widget.children:
        for child in reversed(widget.children):  # Reversed to match widget rendering order
            print_widget_tree(child, level + 1)

class BudgetTracker(BoxLayout):
    pass
class BudgetTrackerApp(App):
    """
    The Kivy App class that manages the application window and content.
    """
    def __init__(self, is_prod=False, **kwargs):
        super().__init__(**kwargs)
        self.content_area = ContentArea()
        self.is_prod = is_prod
        self.outlines_enabled = True
        self.window_state = {
            "size": Window.size,
            "pos": (Window.left, Window.top),
            "is_maximized": False
        }
        self.font_path = os.path.join(os.path.dirname(__file__), "../resources/MaterialSymbolsRounded.ttf")
        self.font_path_extralight = os.path.join(os.path.dirname(__file__), "../resources/MaterialSymbolsRounded-ExtraLight.ttf")
        self.logo = os.path.join(os.path.dirname(__file__), "../resources/BudgetTracker.png")
        self.is_transitioning = False
        
    def change_font_path_callback(self, widget, state):
        if state == "enter":
            widget.font_name = self.font_path
        elif state == "leave":
            widget.font_name = self.font_path_extralight

    def build(self):


        root = BudgetTracker()
        appbar = root.ids.app_bar
        appbar.app = self

        Window.clearcolor = self.hex_to_rgba("#14202E")
        Window.borderless = False
        Window.custom_titlebar = True
        Window.set_custom_titlebar(appbar)
        Window.set_icon(self.logo)
        Window.size = (1280, 720)
        Window.minimum_width = 854
        Window.minimum_height = 480
        Window.left = 300
        Window.top = 150

        hwnd = windll.user32.GetForegroundWindow()
        self.enable_shadow(hwnd)

        return root

    def switch_screen(self, screen_name):
        """Switch to the specified screen."""
        sm = self.root.ids.content_area
        # Determine slide direction based on the target screen
        if sm.current == "dashboard" and screen_name == "transaction":
            sm.transition.direction = "left"  # Slide left when going to transaction
        elif sm.current == "transaction" and screen_name == "dashboard":
            sm.transition.direction = "right"  # Slide right when going back to dashboard

        # Switch screens only if the target screen is different
        if sm.current != screen_name:
            sm.current = screen_name

    def minimize_window(self):
        """Minimize the application window."""
        Window.minimize()

    def maximize_window(self):
        """Maximize or restore the application window."""
        if self.window_state["is_maximized"]:
            # Restore the original size and position
            hwnd = windll.user32.GetForegroundWindow()
            windll.user32.MoveWindow(
                hwnd,
                int(self.window_state["pos"][0]),
                int(self.window_state["pos"][1]),
                int(self.window_state["size"][0]),
                int(self.window_state["size"][1]),
                True,
            )
            self.window_state["is_maximized"] = False
        else:
            # Save the current size and position
            self.window_state["size"] = Window.size[:]
            self.window_state["pos"] = (Window.left, Window.top)

            # Maximize the window
            hwnd = windll.user32.GetForegroundWindow()
            user32 = windll.user32
            user32.SetProcessDPIAware()
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
            windll.user32.MoveWindow(hwnd, 0, 0, screen_width, screen_height, True)
            self.window_state["is_maximized"] = True

    def close_window(self):
        """Close the application window."""
        self.stop()

    @staticmethod
    def enable_shadow(hwnd):
        """Enable a shadow effect for the window."""
        class MARGINS(Structure):
            _fields_ = [("cxLeftWidth", c_int),
                        ("cxRightWidth", c_int),
                        ("cyTopHeight", c_int),
                        ("cyBottomHeight", c_int)]

        margins = MARGINS(-1, -1, -1, -1)
        windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, byref(margins))

    @staticmethod
    def hex_to_rgba(hex_color):
        """Convert a hex color string to an RGBA tuple."""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 8:  # Includes alpha channel
            return [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4, 6)]
        elif len(hex_color) == 6:  # No alpha channel
            return [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)] + [1.0]
        else:
            raise ValueError("Invalid hex color format. Use #RRGGBB or #RRGGBBAA.")

class MARGINS(Structure):
    _fields_ = [("cxLeftWidth", c_int),
                ("cxRightWidth", c_int),
                ("cyTopHeight", c_int),
                ("cyBottomHeight", c_int)]

def enable_shadow(hwnd):
    margins = MARGINS(-1, -1, -1, -1)  # Extend the shadow into the entire window area
    windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, byref(margins))
