from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, BooleanProperty, ListProperty, StringProperty
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color

class HoverBehavior(Widget):
    icon = StringProperty("")
    is_hovered = BooleanProperty(False)
    hover_color = ListProperty([0, 0, 0, 0])
    normal_color = ListProperty([0, 0, 0, 0])
    hover_callback = ObjectProperty(None, allownone=True)
    change_cursor_on_hover = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_move)
        self.background_normal = kwargs.get("background_normal", "")
        self.background_down = kwargs.get("background_down", "")
        self.background_color = kwargs.get("background_color", self.normal_color)
        self.canvas_rectangle = None  # Track the Rectangle instance for custom icons
        
        self.bind(pos=self.update_canvas, size=self.update_canvas, icon=self.update_canvas)


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
        if self.change_cursor_on_hover:
            Window.set_system_cursor("hand")
        if self.hover_callback:
                self.hover_callback(self, "enter")

    def on_leave(self, *args):
        self.is_hovered = False
        self.background_color = self.normal_color
        if HoverBehavior.hovered_widget == self:  # Reset cursor only if this widget was hovered
            HoverBehavior.hovered_widget = None
            if self.change_cursor_on_hover:
                Window.set_system_cursor("arrow")
        if self.hover_callback:
                self.hover_callback(self, "leave")

    def update_canvas(self, *args):
        """Update the button's canvas to draw the custom icon if provided."""
        self.canvas.before.clear()  # Clear previous instructions
        if self.icon:  # Only draw the custom icon if it is provided
            with self.canvas.before:
                Color(1, 1, 1, 1)  # Ensure full opacity for the image
                self.canvas_rectangle = Rectangle(source=self.icon, pos=self.pos, size=self.size)

class HoverableButton(Button, HoverBehavior):
    action_callback = ObjectProperty(None, allownone=True)
    align_text_left = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press=self._on_press_handler)
        if not self.icon:  # Use default behavior if no icon is provided
            self.background_normal = kwargs.get("background_normal", "")
            self.background_down = kwargs.get("background_down", "")
            self.background_color = kwargs.get("background_color", [0, 0, 0, 0])
            # Text alignment properties
            self.text_size = (self.width, None)  # Default text size
            self.halign = "center"  # Default to center alignment
            self.valign = "middle"  # Vertically center the text

            # Dynamically update alignment if `align_text_left` is enabled
            self.bind(
                align_text_left=self._update_alignment,
                size=self._update_alignment,
            )

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
