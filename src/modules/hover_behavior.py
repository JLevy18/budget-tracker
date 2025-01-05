from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty, ListProperty
from kivy.uix.button import Button

class HoverBehavior(Widget):
    is_hovered = BooleanProperty(False)
    hover_color = ListProperty([43 / 255, 66 / 255, 87 / 255, 1])  # Define hover color
    normal_color = ListProperty([0, 0, 0, 0])  # Define normal color

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_move)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = self.normal_color

    def on_mouse_move(self, window, pos):
            """Detect when the mouse enters or leaves the widget."""
            if self.collide_point(*pos):
                if not self.is_hovered:
                    self.on_enter()
            else:
                if self.is_hovered:
                    self.on_leave()


    def on_enter(self, *args):
        self.is_hovered = True
        self.background_color = self.hover_color
        HoverBehavior.hovered_widget = self  # Track the hovered widget
        Window.set_system_cursor("hand")  # Change cursor to hand

    def on_leave(self, *args):
        self.is_hovered = False
        self.background_color = self.normal_color
        if HoverBehavior.hovered_widget == self:  # Reset cursor only if this widget was hovered
            HoverBehavior.hovered_widget = None
            Window.set_system_cursor("arrow")  # Reset cursor to default



class HoverableButton(Button, HoverBehavior):
    pass