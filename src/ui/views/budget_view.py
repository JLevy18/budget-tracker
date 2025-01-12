from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from src.data_manager import get_data_manager


class BudgetView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.active_text_input = None
        self.last_saved_value = None
        self.populate_budget()

    def populate_budget(self):
        data_manager = get_data_manager()
        budget_data = data_manager.get_budget()

        budget_info = self.ids.budget_info
        budget_info.clear_widgets()

        # Add column titles in bold
        column_titles = ["Category", "Name", "Monthly Budget"]
        for title in column_titles:
            budget_info.add_widget(
                Label(text=title, bold=True, font_size=18, size_hint_y=None, height=30)
            )

        # Add budget rows with alternating colors
        row_colors = ["#14202E", "#2B4257"]  # Alternating colors
        for i, (category, name, cost) in enumerate(
            zip(budget_data["Category"], budget_data["Name"], budget_data["Cost per Month"])
        ):
            # Alternate row color
            row_color = row_colors[i % len(row_colors)]

            # Add cells for each row with background color
            self.add_editable_cell(budget_info, category, i, "Category", row_color)
            self.add_editable_cell(budget_info, name, i, "Name", row_color)
            self.add_editable_cell(budget_info, f"${cost:.2f}", i, "Cost per Month", row_color)
    
    def bind_double_click(self, widget, callback):
        """
        Bind double-click behavior to a widget.
        """
        def on_touch_down(instance, touch):
            if touch.is_double_tap and instance.collide_point(*touch.pos):
                callback()

        widget.bind(on_touch_down=on_touch_down)
            
    def add_editable_cell(self, layout, text, row_index, column_name, background_color):
        """
        Add a label cell with inline editing capability.
        """
        label = Label(text=text, size_hint_y=None, height=30)
        with label.canvas.before:
            Color(*self.app.hex_to_rgba(background_color))
            Rectangle(size=label.size, pos=label.pos)
        label.bind(size=self.app.update_rect, pos=self.app.update_rect)

        # Handle double-click to edit only this cell
        self.bind_double_click(label, lambda: self.convert_to_text_input(layout, label, row_index, column_name, background_color))
        layout.add_widget(label)

    def convert_to_text_input(self, layout, instance, row_index, column_name, background_color):
        """
        Replace a label with a TextInput for editing.
        """
        
        if self.active_text_input:
            self.commit_active_text_input()
        
        index = layout.children.index(instance)

        # Replace the clicked label with TextInput
        text_input = TextInput(
            text=instance.text.strip("$"),  # Remove $ for cost editing
            multiline=False,
            size_hint_y=None,
            height=30,
            background_color=(0, 0, 0, 0.2),  # Black background with 0.2 opacity
            foreground_color=(1,1,1,1),
            cursor_color=(1, 1, 1, 1),  # White cursor color
        )
        
        self.last_saved_value = text_input.text

        from kivy.clock import Clock
        
        # Focus and highlight the text
        def focus_and_highlight(dt):
            text_input.focus = True
            text_input.select_all()

        Clock.schedule_once(focus_and_highlight, 0)        
        
        text_input.bind(
            on_text_validate=lambda widget: self.on_text_input_enter(
                widget, row_index, column_name, background_color, layout, index
            )
        )
        text_input.bind(
            focus=lambda instance, focus: self.on_focus_lost(instance, focus)
        )
        text_input.bind(size=self.app.update_rect, pos=self.app.update_rect)

        layout.remove_widget(instance)
        layout.add_widget(text_input, index=index)
        
        self.active_text_input = (text_input, layout, row_index, column_name, background_color, index)
        
    def on_focus_lost(self, instance, focus):
        """
        Commit changes when the TextInput loses focus.
        """
        if not focus and self.active_text_input:
            if instance.text.strip() != self.last_saved_value:
                # Commit changes if the value has changed
                self.commit_active_text_input()
            else:
                # Revert without committing if no changes
                self.revert_to_label()
    
    def revert_to_label(self):
        """
        Revert the active TextInput to a Label without saving.
        """
        if not self.active_text_input:
            return

        widget, layout, row_index, column_name, background_color, index = self.active_text_input
        new_value = self.last_saved_value
        layout.remove_widget(widget)

        # Add the original Label back
        label = Label(text=new_value, size_hint_y=None, height=30)
        with label.canvas.before:
            Color(*self.app.hex_to_rgba(background_color))
            Rectangle(size=label.size, pos=label.pos)
        label.bind(size=self.app.update_rect, pos=self.app.update_rect)
        self.bind_double_click(label, lambda: self.convert_to_text_input(layout, label, row_index, column_name, background_color))
        layout.add_widget(label, index=index)
        self.active_text_input = None  # Clear active state
    
    def commit_active_text_input(self):
        """
        Commit changes for the currently active TextInput.
        """
        if not self.active_text_input:
            return

        widget, layout, row_index, column_name, background_color, index = self.active_text_input
        self.on_text_input_enter(widget, row_index, column_name, background_color, layout, index)
        self.active_text_input = None
    
    def on_text_input_enter(self, widget, row_index, column_name, background_color, layout, index):
        """
        Handle saving data when the user presses Enter and update the table correctly.
        """
        new_value = widget.text.strip()
        
        if not new_value:
            new_value = self.last_saved_value

        # Update the data in the DataManager
        data_manager = get_data_manager()
        budget_data = data_manager.get_budget()
        if column_name == "Category":
            budget_data["Category"][row_index] = new_value
        elif column_name == "Name":
            budget_data["Name"][row_index] = new_value
        elif column_name == "Cost per Month":
            # Ensure valid float conversion for costs
            try:
                value_as_float = float(new_value) if new_value else 0.0  # Default to 0.0 if empty
                budget_data["Cost per Month"][row_index] = round(value_as_float, 2)
                new_value = f"${value_as_float:.2f}"  # Format as currency
            except ValueError:
                # Revert to the original value if input is invalid
                value_as_float = budget_data["Cost per Month"][row_index]
                new_value = f"${value_as_float:.2f}"

        # Save the updated data back to the data file
        data_manager.set_budget(budget_data)

        # Replace the TextInput with a new Label at the same index
        layout.remove_widget(widget)
        label = Label(text=new_value, size_hint_y=None, height=30)
        with label.canvas.before:
            Color(*self.app.hex_to_rgba(background_color))
            Rectangle(size=label.size, pos=label.pos)
        label.bind(size=self.app.update_rect, pos=self.app.update_rect)
        self.bind_double_click(label, lambda: self.convert_to_text_input(layout, label, row_index, column_name, background_color))
        layout.add_widget(label, index=index)  # Add the new Label back at the exact same position
        self.active_text_input = None
