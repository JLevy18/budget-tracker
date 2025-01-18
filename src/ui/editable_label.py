from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.clock import Clock

class EditableLabel(BoxLayout):
    text = StringProperty("")  # Allow text to be set from KV
    text_align = StringProperty("left")
    auto_highlight = BooleanProperty(True)
    auto_commit = BooleanProperty(True)
    text_color = ListProperty([1,1,1,1])
    cursor_color = ListProperty([])
    background_color = ListProperty([0,0,0,0.25])
    on_text_commit = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(orientation="horizontal", **kwargs)
        
        
        self.size_hint_y: None
        self.bind(on_touch_up=self.on_double_click)
        
        
        self.label = Label(valign="middle")
        self.label.bind(size=self.update_alignment)
        self.bind(text=self.update_text)
        self.bind(text_align=self.update_alignment)
        
        self.add_widget(self.label)
        self.update_text()
        self.update_alignment()

    def on_double_click(self, instance, touch):
        """Detect double-clicks on the entire BoxLayout."""
        if touch.is_double_tap and self.collide_point(*touch.pos):
            self.convert_to_text_input()
    
    
    def convert_to_text_input(self):
        """Replace the label with a TextInput in the same space."""
        # Remove existing label
        self.remove_widget(self.label)

        cursor_color = self.cursor_color if self.cursor_color else self.text_color

        # Create a TextInput with the same properties
        self.text_input = TextInput(
            text=self.text,
            center_y=1,
            multiline=False,
            size_hint=(1, 1),  # Matches BoxLayout constraints
            foreground_color=self.text_color,
            cursor_color=cursor_color,
            background_color=self.background_color,
        )

        self.text_input.bind(focus=self.on_unfocus)
    
        # Add the text input in place of the label
        self.add_widget(self.text_input)
        Clock.schedule_once(self.set_focus, 0.1)

    def set_focus(self, dt):
        """Ensure TextInput gets proper focus."""
        self.text_input.focus = True
        if self.auto_highlight:
            self.text_input.select_all()

    def on_unfocus(self, instance, focus):
        """Called when TextInput loses focus."""
        if not focus and self.auto_commit:  # If focus is lost
            self.commit_text()

    def commit_text(self):
        """Save text and switch back to label mode."""
        new_value = self.text_input.text.strip()
        if new_value and new_value != self.text:
            self.text = new_value
            if self.on_text_commit:
                self.on_text_commit(new_value)  # Call the function from KV

        # Remove TextInput and restore label
        self.remove_widget(self.text_input)
        self.add_widget(self.label)

    def update_text(self, *args):
        """Update label text dynamically"""
        self.label.text = self.text  # Sync label with `text` property
        self.label.text_size = (self.width, None)

    def update_alignment(self, *args):
        """Update label alignment dynamically"""
        if self.text_align in ["left", "center", "right"]:
            self.label.halign = self.text_align
            self.label.text_size = (self.width, None)
        else:
            self.label.halign = "left"  # Default to left if invalid