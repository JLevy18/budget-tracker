from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, BooleanProperty, ListProperty, StringProperty
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color
from kivy.animation import Animation

class HoverBehavior(Widget):
    is_hovered = BooleanProperty(False)
    transition = StringProperty(None)
    hover_color = ListProperty([0, 0, 0, 0])
    normal_color = ListProperty([0, 0, 0, 0])
    hover_callback = ObjectProperty(None, allownone=True)
    change_cursor_on_hover = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_move)
        self.app = App.get_running_app()
        self.background_normal = kwargs.get("background_normal", "")
        self.background_down = kwargs.get("background_down", "")
        self.background_color = kwargs.get("background_color", self.normal_color)


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
        if self.transition == "smooth":
            Animation.cancel_all(self)
            Animation(background_color=self.hover_color, duration=0.3, t="out_expo").start(self)
        else:
            self.background_color = self.hover_color
        HoverBehavior.hovered_widget = self  # Track the hovered widget
        if self.change_cursor_on_hover:
            Window.set_system_cursor("hand")
        if self.hover_callback:
            self.hover_callback(self, "enter")

    def on_leave(self, *args):
        self.is_hovered = False
        if self.transition == "smooth":
            Animation.cancel_all(self)
            Animation(background_color=self.normal_color, duration=1, t="out_expo").start(self)
        else:
            self.background_color = self.normal_color
        if HoverBehavior.hovered_widget == self:  # Reset cursor only if this widget was hovered
            HoverBehavior.hovered_widget = None
            if self.change_cursor_on_hover:
                Window.set_system_cursor("arrow")
        if self.hover_callback:
                self.hover_callback(self, "leave")

class HoverableButton(Button, HoverBehavior):
    action_callback = ObjectProperty(None, allownone=True)
    align_text_left = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press=self._on_press_handler)
        
        self.register_event_type("on_enter")
        self.register_event_type("on_leave")
        
        Window.bind(mouse_pos=self.on_mouse_move)
        # Text alignment properties
        self.text_size = (self.width, None)  # Default text size
        self.halign = "center"  # Default to center alignment
        self.valign = "middle"  # Vertically center the text

        # Dynamically update alignment if `align_text_left` is enabled
        self.bind(
            align_text_left=self._update_alignment,
            size=self._update_alignment,
            )

    def on_mouse_move(self, window, pos):
        """Detect when the mouse enters or leaves the button."""
        if self.collide_point(*self.to_widget(*pos)):  # Convert screen pos to local pos
            if not self.is_hovered:
                self.dispatch("on_enter")
        else:
            if self.is_hovered:
                self.dispatch("on_leave")

    def _update_alignment(self, *args):
        """Update text alignment dynamically based on `align_text_left`."""
        if self.align_text_left:
            self.text_size = (self.width - 10, None)  # Add padding for the text area
            self.halign = "left"
        else:
            self.text_size = (self.width, None)  # Reset to full width
            self.halign = "center"
    def _on_press_handler(self, *args):
        """Call the action callback if provided."""
        if self.action_callback:
            self.action_callback(self)
    
    def change_font_path_callback(self, root, widget, state):
        from src.modules.nav_bar import NavBar
        if isinstance(root, NavBar):
            if widget == root.selected_button:
                # Don't change the font of the selected button
                return

        if state == "enter":
            widget.font_name = self.app.font_path
        elif state == "leave":
            widget.font_name = self.app.font_path_extralight