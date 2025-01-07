
import os
import sys

from kivy.app import App
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.layout import Layout
from kivy.graphics import Color, Line

from src.modules.app_bar import AppBar
from src.modules.content_area import ContentArea
from src.modules.hover_behavior import HoverableButton
from src.modules.classes.budget import Budget
from src.content_factory import ContentFactory

from ctypes import windll, Structure, c_int, byref



OUTLINE_COLORS = [
    ((1, 0, 0, 1), "Red"),        # Red
    ((1, 0.5, 0, 1), "Orange"),    # Orange
    ((1, 1, 0, 1), "Yellow"),     # Yellow
    ((0, 1, 0, 1), "Green"),      # Green
    ((0, 0, 1, 1), "Blue"),       # Blue
    ((0, 1, 1, 1), "Cyan"),       # Cyan
    ((0.5, 0, 0.5, 1), "Purple"),  # Purple
    ((1, 0, 1, 1), "Magenta"),    # Magenta
    ((0.5, 0.5, 0.5, 1), "Gray"), # Gray
    
    ((0.5, 0, 0, 1), "Dark Red"), # Dark Red
    ((0, 0.5, 0, 1), "Dark Green"), # Dark Green
    ((0, 0, 0.5, 1), "Dark Blue"), # Dark Blue
]

displayed_levels = set({0,1,2,3,4,5,6,7,8})

# Determine base paths
if getattr(sys, "frozen", False):  # If running in a PyInstaller bundle
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  # Current script's directory

KV_DIR = os.path.join(base_path, "ui")
Builder.load_file(os.path.join(KV_DIR, "budget_tracker.kv"))

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'dpi', 'auto')
Config.set('kivy', 'window', 'sdl2')
Config.set('graphics', 'show_fps', '1')
Config.set('modules', 'monitor', '1')

Factory.register("HoverableButton", cls=HoverableButton)
Factory.register("ContentArea", cls=ContentArea)

def initialize_app(base_dir, is_prod):
    """
    Initialize the application by ensuring directories exist and loading the budget.
    """
    content_factory = ContentFactory()  # Initialize content factory

    return BudgetTrackerApp(content_factory, is_prod=is_prod)


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
    def __init__(self, content_factory, is_prod=False, **kwargs):
        super().__init__(**kwargs)
        self.content_factory = content_factory  # Factory for creating content pages
        self.content_area = None
        self.is_prod = is_prod
        self.outlines_enabled = True
        self.window_state = {
            "size": Window.size,
            "pos": (Window.left, Window.top),
            "is_maximized": False
        }
        self.font_path = os.path.join(os.path.dirname(__file__), "../resources/MaterialRounded.ttf")
        self.logo = os.path.join(os.path.dirname(__file__), "../resources/BudgetTracker.png")

    def build(self):

        Window.clearcolor = self.hex_to_rgba("#14202E")
        Window.borderless = False
        Window.custom_titlebar = True
        appbar = AppBar()
        appbar.app = self
        Window.set_custom_titlebar(appbar)
        Window.set_icon(self.logo)
        Window.size = (1280, 720)
        Window.minimum_width = 854
        Window.minimum_height = 480
        Window.left = 300
        Window.top = 150

        hwnd = windll.user32.GetForegroundWindow()
        self.enable_shadow(hwnd)

        if not self.is_prod:
            Window.bind(on_key_down=self.on_key_down)

        root = BudgetTracker()
        self.content_area = root.ids.content_area
        self.load_page("dashboard")
        toggle_outlines(root, self.outlines_enabled)
        return root

    def load_page(self, page_name):
        """Swap the content area to display a specific page."""
        content = self.content_factory.create(page_name)
        if content:
            self.content_area.swap_content(content)

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        """Handle key presses for toggling outlines."""
        if key == 284:
            self.outlines_enabled = not self.outlines_enabled
            toggle_outlines(self.root, self.outlines_enabled)

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
        return [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)] + [1]

class MARGINS(Structure):
    _fields_ = [("cxLeftWidth", c_int),
                ("cxRightWidth", c_int),
                ("cyTopHeight", c_int),
                ("cyBottomHeight", c_int)]

def enable_shadow(hwnd):
    margins = MARGINS(-1, -1, -1, -1)  # Extend the shadow into the entire window area
    windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, byref(margins))

def add_outlines_to_layouts(widget, enable, level=0):
    """Recursively add outlines to all layouts."""
    if not enable:  # If outlines are disabled, clear all
        clear_outlines(widget)
        return

    color, color_name = OUTLINE_COLORS[level % len(OUTLINE_COLORS)]
    if level not in displayed_levels:  # Display level color only once
        print(f"Level {level}: Color is {color_name}")
        displayed_levels.add(level)

    if isinstance(widget, Layout):
        with widget.canvas.before:
            Color(*color)  # Red outline color
            Line(rectangle=(widget.x, widget.y, widget.width, widget.height), width=1)
        widget.bind(pos=lambda instance, value: update_outline(instance, color))
        widget.bind(size=lambda instance, value: update_outline(instance, color))
    
    for child in widget.children:
        add_outlines_to_layouts(child, enable, level + 1)

def update_outline(widget, color):
    """Update the outline to match the widget's size and position."""
    widget.canvas.before.clear()
    with widget.canvas.before:
        Color(*color)  # Red outline color
        Line(rectangle=(widget.x, widget.y, widget.width, widget.height), width=1)

def clear_outlines(widget):
    """Clear outlines from all layouts."""
    if isinstance(widget, Layout):
        widget.canvas.before.clear()
    for child in widget.children:
        clear_outlines(child)

def toggle_outlines(widget, enable):
    """Enable or disable outlines for all layouts."""
    if enable:
        add_outlines_to_layouts(widget, enable=True)  # Reuse the modified add_outlines_to_layouts function
    else:
        clear_outlines(widget)
        displayed_levels.clear()