from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.graphics import Color, Line
from kivy.utils import platform
from src.modules.appbar import AppBar
from src.modules.hover_behavior import HoverableButton
from ctypes import windll, Structure, c_int, byref
from itertools import cycle

# Register the class with Kivy
import os
import sys

OUTLINE_COLORS = cycle([
    (1, 0, 0, 1),  # Red
    (0, 1, 0, 1),  # Green
    (0, 0, 1, 1),  # Blue
    (1, 1, 0, 1),  # Yellow
    (1, 0, 1, 1),  # Magenta
    (0, 1, 1, 1),  # Cyan
    (0.5, 0.5, 0.5, 1),  # Gray
])

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

def add_outlines_to_layouts(widget, enable, color_cycle=None):
    """Recursively add outlines to all layouts."""
    if color_cycle is None:
        color_cycle = OUTLINE_COLORS  # Use the global color cycle
    if not enable:  # If outlines are disabled, clear all
        clear_outlines(widget)
        return
    if isinstance(widget, Layout):
        with widget.canvas.before:
            Color(*next(color_cycle))  # Red outline color
            Line(rectangle=(widget.x, widget.y, widget.width, widget.height), width=1)
        widget.bind(pos=lambda instance, value: update_outline(instance, color_cycle))
        widget.bind(size=lambda instance, value: update_outline(instance, color_cycle))
    
    for child in widget.children:
        add_outlines_to_layouts(child, enable, color_cycle)

def update_outline(widget, color_cycle):
    """Update the outline to match the widget's size and position."""
    color = next(color_cycle)  # Get the next color from the cycle
    print(f"Updating outline: Widget={widget.__class__.__name__}, Color={color}")  # Print widget info and color
    widget.canvas.before.clear()
    with widget.canvas.before:
        Color(*color)  # Red outline color
        Line(rectangle=(widget.x, widget.y, widget.width, widget.height), width=1.5)

def clear_outlines(widget):
    """Clear outlines from all layouts."""
    if isinstance(widget, Layout):
        widget.canvas.before.clear()
    for child in widget.children:
        clear_outlines(child)

def toggle_outlines(widget, enable, color_cycle=None):
    """Enable or disable outlines for all layouts."""
    if color_cycle is None:
        color_cycle = OUTLINE_COLORS  # Use the global color cycle

    if isinstance(widget, Layout):
        if enable:
            widget.bind(pos=lambda instance, value: update_outline(instance, color_cycle))
            widget.bind(size=lambda instance, value: update_outline(instance, color_cycle))
            update_outline(widget, color_cycle)  # Initial outline update
        else:
            widget.unbind(pos=None, size=None)  # Unbind updates
            widget.canvas.before.clear()

    for child in widget.children:
        toggle_outlines(child, enable, color_cycle)

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
    def __init__(self, budget, is_prod=False, **kwargs):
        super().__init__(**kwargs)
        self.budget = budget
        self.is_prod = is_prod
        self.outlines_enabled = False
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
        Window.set_custom_titlebar(AppBar())
        Window.set_icon(os.path.join(os.path.dirname(__file__), "../resources/BudgetTracker.ico"))

        hwnd = windll.user32.GetForegroundWindow()
        enable_shadow(hwnd)

        if not self.is_prod:
            Window.bind(on_key_down=self.on_key_down)

        root = DashboardScreen(self.budget)
        return root

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        """Handle key presses."""
        if key == 284:
            self.outlines_enabled = not self.outlines_enabled
            toggle_outlines(self.root, self.outlines_enabled)

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