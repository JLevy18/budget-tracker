from kivy.app import App


from kivy.config import Config
from kivy.core.window import Window

from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.graphics import Color, Line
from kivy.utils import platform
from src.modules.appbar import AppBar

from ctypes import windll, Structure, c_int, byref


# Register the class with Kivy
import os



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