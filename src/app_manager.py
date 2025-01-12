
import os
import sys
import random

from kivy.app import App
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.layout import Layout
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition, FadeTransition
from kivy.graphics import Color, Line, Rectangle

from src.modules.app_bar import AppBar
from src.modules.nav_bar import NavBar
from src.modules.content_area import ContentArea
from src.modules.hover_behavior import HoverableButton
from src.data_manager import DataManager, set_data_manager

from ctypes import windll, Structure, c_int, byref

# Determine base paths
if getattr(sys, "frozen", False):  # If running in a PyInstaller bundle
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  # Current script's directory

KV_DIR = os.path.join(base_path, "ui")
Builder.load_file(os.path.join(KV_DIR, "budget_tracker.kv"))
Builder.load_file(os.path.join(KV_DIR, "app_bar.kv"))
Builder.load_file(os.path.join(KV_DIR, "views", "budget_view.kv"))
Builder.load_file(os.path.join(KV_DIR, "views", "dashboard_view.kv"))
Builder.load_file(os.path.join(KV_DIR, "views", "transaction_view.kv"))

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'dpi', 'auto')
Config.set('kivy', 'window', 'sdl2')

def initialize_app(base_dir, is_prod):
    """
    Initialize the application by setting up the data manager and returning the app instance.
    """
    # Initialize the data manager
    data_manager = DataManager(base_dir, is_prod)
    
    # Load profiles or create default if none exist
    profiles = data_manager.get_profiles()
    if not profiles:
        default_file = data_manager.create_new_profile(income=5000.00)
        data_manager.load_data(default_file)
    else:
        # Set the first profile as the active one by default
        data_manager.load_data(profiles[0]["path"])

    # Pass the data manager to the app
    app = BudgetTrackerApp(data_manager=data_manager, is_prod=is_prod)

    return data_manager, app
class BudgetTracker(BoxLayout):
    pass
class BudgetTrackerApp(App):
    """
    The Kivy App class that manages the application window and content.
    """
    def __init__(self, data_manager, is_prod=False, **kwargs):
        super().__init__(**kwargs)
        self.content_area = ContentArea()
        self.is_prod = is_prod
        self.background_toggle = False
        self.window_state = {
            "size": Window.size,
            "pos": (Window.left, Window.top),
            "is_maximized": False
        }
        self.font_path = os.path.join(os.path.dirname(__file__), "../resources/MaterialSymbolsRounded.ttf")
        self.font_path_extralight = os.path.join(os.path.dirname(__file__), "../resources/MaterialSymbolsRounded-ExtraLight.ttf")
        self.logo = os.path.join(os.path.dirname(__file__), "../resources/BudgetTracker.png")
        self.is_transitioning = False
        
        set_data_manager(data_manager)
    
    
    def toggle_background_colors(self):
        """Toggle background colors for all widgets."""
        self.background_toggle = not  self.background_toggle
        self.apply_background_colors(self.root)

    def apply_background_colors(self, widget):
        """Recursively apply background colors to the widget tree."""
        with widget.canvas.before:
            if self.background_toggle:
                # Generate a random neon color (bright, high-saturation RGB) with low opacity
                r, g, b = random.choices([0, 1], k=3)  # Returns a list of three elements
                Color(r, g, b, 0.3)  # 30% opacity
            else:
                Color(1, 1, 1, 0)

            # Redraw the rectangle
            Rectangle(size=widget.size, pos=widget.pos)

            
        # Recurse for child widgets
        for child in widget.children:
            self.apply_background_colors(child)
                
    def change_font_path_callback(self, widget, state):
        if state == "enter":
            widget.font_name = self.font_path
        elif state == "leave":
            widget.font_name = self.font_path_extralight

    def build(self):

        root = BudgetTracker()
        appbar = root.ids.app_bar
        appbar.app = self
        titlebar = appbar.ids.title_bar
        Window.clearcolor = self.hex_to_rgba("#14202E")
        Window.borderless = True
        Window.custom_titlebar = True
        Window.set_custom_titlebar(titlebar)
        Window.set_icon(self.logo)
        Window.size = (1280, 720)
        Window.minimum_width = 854
        Window.minimum_height = 480
        Window.left = 300
        Window.top = 150
        
        Window.bind(on_key_down=self.on_key_down)

        hwnd = windll.user32.GetForegroundWindow()
        self.enable_shadow(hwnd)

        return root
    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 284:  # Keycode for F3
            self.toggle_background_colors()

    def switch_screen(self, screen_name):
        """Switch to the specified screen."""
        sm = self.root.ids.content_area

        # Define the order of the screens
        screen_order = ["dashboard", "transaction", "settings"]

        # Get the current and target indices
        current_index = screen_order.index(sm.current)
        target_index = screen_order.index(screen_name)

        # Determine swipe direction based on indices
        if current_index < target_index:
            sm.transition.direction = "left"  # Swipe left to move forward
        elif current_index > target_index:
            sm.transition.direction = "right"  # Swipe right to move backward

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
