from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import BooleanProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.button import Button
from src.modules.hover_behavior import HoverableButton
from ctypes import windll, Structure, c_long, byref
import os
import sys

# Ensure the KV file is loaded
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Move up one level to 'src'

if getattr(sys, "frozen", False):  # If running in a PyInstaller bundle
    KV_DIR = os.path.join(sys._MEIPASS, "src", "ui")
else:
    KV_DIR = os.path.join(BASE_DIR, "ui")  # Resolve to 'src/ui'

Builder.load_file(os.path.join(KV_DIR, "titlebar.kv"))

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def get_cursor_pos():
    """Get the global cursor position in DPI-aware coordinates."""
    point = POINT()
    windll.user32.GetCursorPos(byref(point))
    return point.x, point.y

class TitleBar(BoxLayout):
    is_dragging = False
    drag_start_pos = None
    initial_window_pos = None

    def on_touch_down(self, touch):
        local_pos = self.to_widget(*touch.pos)

        if self.collide_point(*local_pos):
            for child in self.children:
                # Skip AnchorLayouts
                if isinstance(child, AnchorLayout) and child.collide_point(*touch.pos):
                    for sub_child in child.children:
                        if sub_child.collide_point(*touch.pos):
                            print(f"Touch is on interactive widget: {sub_child}")
                            return super().on_touch_down(touch)

            self.is_dragging = True
            user32 = windll.user32
            user32.SetProcessDPIAware()
            
            self.initial_window_pos = (Window.left, Window.top)
            self.cursor_start_pos = get_cursor_pos()

            return True  
        return super().on_touch_down(touch)
    def on_touch_move(self, touch):
        # Drag the window if dragging is active
        if self.is_dragging:
            current_cursor_pos = get_cursor_pos()

            # Calculate the delta
            dx = current_cursor_pos[0] - self.cursor_start_pos[0]
            dy = current_cursor_pos[1] - self.cursor_start_pos[1]

            # Calculate the new window position
            new_x = self.initial_window_pos[0] + dx
            new_y = self.initial_window_pos[1] + dy
            
            hwnd = windll.user32.GetForegroundWindow()
            windll.user32.MoveWindow(hwnd, int(new_x), int(new_y), int(Window.width), int(Window.height), True)
            
            return True  # Consume the event
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        # Stop dragging
        if self.is_dragging:
            self.is_dragging = False
            return True  # Consume the event
        return super().on_touch_up(touch)