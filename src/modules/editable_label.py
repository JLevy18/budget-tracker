from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, ListProperty, NumericProperty
from kivy.clock import Clock
import re

class EditableLabel(BoxLayout):
    text = StringProperty("")  # Allow text to be set from KV
    text_align = StringProperty("left")
    text_color = ListProperty([1,1,1,1])
    text_format = StringProperty(None)
    font_size = NumericProperty(16)
    auto_highlight = BooleanProperty(True)
    auto_commit = BooleanProperty(True)
    cursor_color = ListProperty([])
    background_color = ListProperty([0,0,0,0.25])
    max_content = NumericProperty(None)
    max_length = NumericProperty(None)
    bold = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(orientation="horizontal", **kwargs)
        self.register_event_type("on_commit")
        
        self.size_hint_y: None
        self.text_input = None
        self.previous_text = self.text
        self.bind(on_touch_up=self.on_double_click)
        
        
        self.label = Label()
        self.label.bind(size=self.update_alignment)
        self.bind(bold=self.update_font_weight)
        self.bind(text=self.update_text)
        self.bind(font_size=self.update_font_size)
        self.bind(text_align=self.update_alignment)
        self.bind(max_content=self.update_label_size)
        
        self.add_widget(self.label)
        self.update_label_size()
        self.update_text()
        self.update_alignment()
        
    def on_commit(self, new_text): pass
    
    def on_double_click(self, instance, touch):
        """Detect double-clicks on the entire BoxLayout."""
        if touch.is_double_tap and self.collide_point(*touch.pos):
            if self.text_input:  # If already editing, commit instead of recreating
                self.commit_text()
            else:
                self.convert_to_text_input()
    
    
    def convert_to_text_input(self):
        """Replace the label with a TextInput in the same space."""
        # Remove existing label
        self.remove_widget(self.label)

        cursor_color = self.cursor_color if self.cursor_color else self.text_color

        # Create a TextInput with the same properties
        self.text_input = TextInput(
            text=self.text,
            multiline=False,
            size_hint=(1, 1),  # Matches BoxLayout constraints
            foreground_color=self.text_color,
            cursor_color=cursor_color,
            background_color=self.background_color,
        )

        if self.max_length:
            self.text_input.bind(text=self.validate_text_length)

        self.text_input.bind(focus=self.on_unfocus)
    
        # Add the text input in place of the label
        self.add_widget(self.text_input)
        Clock.schedule_once(self.set_focus, 0.1)

    def set_focus(self, dt):
        """Ensure TextInput gets proper focus."""
        self.text_input.focus = True
        if self.auto_highlight:
            self.text_input.select_all()

    def validate_text_length(self, instance, value):
        """Prevent exceeding max_length and dispatch notification event."""
        if self.max_length and len(value) > self.max_length:
            instance.text = instance.text[:self.max_length]
            self.dispatch("on_text_exceed_limit", value)

    def on_unfocus(self, instance, focus):
        """Called when TextInput loses focus."""
        if not focus and self.auto_commit:  # If focus is lost
            self.commit_text()

    def commit_text(self):
        """Save text and switch back to label mode."""
        if not self.text_input:  # Prevent crashes when spam clicking
            return
        
        new_value = self.text_input.text.strip() if self.text_input.text else ""

        if self.is_money_field():
            if not self.is_valid_money(new_value):
                print("Invalid money input detected. Reverting to previous value.")
                new_value = self.previous_text  # Revert to last valid text
            else:
                new_value = self.format_money(new_value)
        
        if new_value and new_value != self.text:
            self.text = new_value
            self.dispatch("on_commit", new_value)  # Dispatch the event

        # Remove TextInput and restore label
        if self.text_input in self.children:
            self.remove_widget(self.text_input)
        self.text_input = None  # Reset the TextInput reference

        # Create and add a new label
        self.create_label()
        self.add_widget(self.label)
        
    def is_money_field(self):
        return self.text_format == "money"

    def is_valid_money(self, value):
        """Check if the value is a valid money format (only numbers, decimals, commas, and $ signs)."""
        if re.search(r"[a-zA-Z]", value):  # Reject if letters are present
            return False
        if value.count(".") > 1:  # Reject if more than one decimal
            return False
        return True
    
    def update_font_size(self, *args):
        """Ensure font size updates dynamically in committed label."""
        self.label.font_size = self.font_size
    
    def update_font_weight(self, *args):
        self.label.bold = self.bold
    
    def format_text(self, text):
        """Format the text based on its content."""
        text = text.strip()

        if not text:
            return ""

        # Capitalize the first letter of text
        return text.capitalize()

    def format_money(self, value):
        """Format money values as $X,XXX.XX"""
        # Remove all non-numeric characters except decimal points
        value = re.sub(r"[^\d.]", "", value)

        try:
            # Convert to float and round to two decimal places
            formatted_value = "${:,.2f}".format(round(float(value), 2))
            return formatted_value
        except ValueError:
            return self.previous_text  # Revert if invalid

    def create_label(self):
        """Create a new Label instance."""
        self.label = Label(
            text=self.truncate_text(self.text),
            bold=self.bold,
            halign=self.text_align,
            size_hint=(1, 1),
        )
        self.label.bind(size=self.update_alignment)

    def truncate_text(self, text):
        """Truncate text with '...' if it's too long for the label's width."""
        if not self.label:
            return text
        
        estimated_chars = int((self.label.width + 10) / 8) # Approximate 8px per character
        if self.max_content and self.width >= self.max_content:
            if len(text) > estimated_chars:
                return text[: estimated_chars - 3] + "..."
        return text

    def update_label_size(self, *args):
        """Dynamically update label width based on text length."""
        text_width = self.get_text_width()
        # Ensure label width does not exceed max_content if set
        if self.max_content and text_width > self.max_content:
            self.width = self.max_content
        else:
            self.width = text_width

    def get_text_width(self):
        """Estimate text width dynamically."""
        estimated_width = (len(self.text) * 8)  # Approximate width in pixels
        return min(estimated_width, self.max_content) if self.max_content else estimated_width

    def update_text(self, *args):
        """Update label text dynamically"""
        self.update_label_size()
        self.label.text = self.truncate_text(self.text)  # Sync label with `text` property
        self.label.text_size = (self.width, None)

    def update_alignment(self, *args):
        """Update label alignment dynamically"""
        if self.text_align in ["left", "center", "right"]:
            self.label.halign = self.text_align
            self.label.text_size = (self.width, None)
        else:
            self.label.halign = "left"  # Default to left if invalid