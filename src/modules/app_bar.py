from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from src.modules.hover_behavior import HoverableButton
from ctypes import windll, Structure, c_long, byref
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if getattr(sys, "frozen", False):  # If running in a PyInstaller bundle
    # Resolve `src/ui` relative to the PyInstaller bundle
    KV_DIR = os.path.join(sys._MEIPASS, "ui")
else:
    # Resolve `src/ui` relative to the current script's directory
    KV_DIR = os.path.join(BASE_DIR, "ui")

Builder.load_file(os.path.join(KV_DIR, "app_bar.kv"))

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def get_cursor_pos():
    """Get the global cursor position in DPI-aware coordinates."""
    point = POINT()
    windll.user32.GetCursorPos(byref(point))
    return point.x, point.y

def get_tallest_child_with_padding(widget):
    """Recursively find the tallest child with an explicit height and its padding."""
    if hasattr(widget, "children") and widget.children:
        tallest_height = 0
        padding_top = 0
        padding_bottom = 0

        for child in widget.children:
            child_height, child_padding_top, child_padding_bottom = get_tallest_child_with_padding(child)
            if child_height > tallest_height:
                tallest_height = child_height
                padding_top = child_padding_top
                padding_bottom = child_padding_bottom

        # If the widget itself has padding (e.g., it's a layout), use its padding
        if hasattr(widget, "padding") and isinstance(widget.padding, (list, tuple)):
            padding_top += widget.padding[1] if len(widget.padding) > 1 else 0
            padding_bottom += widget.padding[3] if len(widget.padding) > 3 else 0

        return tallest_height, padding_top, padding_bottom

    elif hasattr(widget, "height") and widget.size_hint_y is None:
        return widget.height, 0, 0  # Fixed height, no padding

    return 0, 0, 0  # Default to 0 if no valid height is found

def get_youngest_child(widget, touch):
    """Recursively find the youngest (deepest) child that collides with the touch point."""
    if hasattr(widget, "children") and widget.children:
        for child in widget.children:
            if child.collide_point(*touch.pos):
                # Recurse into the child widget
                return get_youngest_child(child, touch)
    # If no children collide, return the widget itself
    return widget

def is_draggable(widget, touch):
    """Check if the widget under the touch point is draggable."""
    # Find the youngest (deepest) child
    target_widget = get_youngest_child(widget, touch)
    # Check if the target widget is draggable

    if isinstance(target_widget, (Button, HoverableButton)):
        return False
    
    if isinstance(target_widget, AnchorLayout):
        return True
    
    if isinstance(target_widget, Label):
        return True

    # Default: Disallow dragging for other widget types
    return False

class AppBar(BoxLayout):
    is_dragging = False
    drag_start_pos = None
    initial_window_pos = None

    def on_size(self, *args):
        """Dynamically adjust TitleBar height based on its tallest child plus padding."""
        # Calculate the tallest child and padding
        tallest_child_height, padding_top, padding_bottom = get_tallest_child_with_padding(self)

        # Add padding to the total height
        total_height = tallest_child_height + padding_top + padding_bottom

        # Update the height of the TitleBar
        self.height = total_height

    def on_touch_down(self, touch):
        local_pos = self.to_widget(*touch.pos)

        if self.collide_point(*local_pos):
            # Check if the touch is on a draggable widget
            if is_draggable(self, touch):
                self.is_dragging = True
                user32 = windll.user32
                user32.SetProcessDPIAware()
                
                self.initial_window_pos = (Window.left, Window.top)
                self.cursor_start_pos = get_cursor_pos()

                return True
            else:
                return super().on_touch_down(touch)

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