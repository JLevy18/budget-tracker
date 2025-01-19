from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from src.data_manager import get_data_manager
from src.modules.editable_label import EditableLabel


class BudgetView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.data_manager = get_data_manager()
        self.active_text_input = None
        self.last_saved_value = None
        self.populate_budget()
    
    def populate_budget(self):
        budget_data = self.data_manager.get_budget()

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
    
            
    def add_editable_cell(self, layout, text, row_index, column_name, background_color):
        """
        Add a label cell with inline editing capability.
        """
        editable_label = None
        if (column_name == "Cost per Month"):
            editable_label = EditableLabel(
                text=text,
                text_align="center",
                text_format="money",
            )
        else:
            editable_label = EditableLabel(
                text=text,
                text_align="center",
            )

        editable_label.bind(on_commit=lambda instance, new_text: self.update_budget_data(new_text, row_index, column_name))

        with editable_label.canvas.before:
            Color(*self.app.hex_to_rgba(background_color))
            Rectangle(size=editable_label.size, pos=editable_label.pos)

        editable_label.bind(size=self.app.update_rect, pos=self.app.update_rect)

        layout.add_widget(editable_label)


    def update_budget_data(self, new_text, row_index, column_name):
        budget_data = self.data_manager.get_budget()
        if column_name == "Category":
            budget_data["Category"][row_index] = new_text
        elif column_name == "Name":
            budget_data["Name"][row_index] = new_text
        elif column_name == "Cost per Month":
            try:
                budget_data["Cost per Month"][row_index] = round(float(new_text.replace("$", "")), 2)
            except ValueError:
                pass  # Ignore invalid input

        self.data_manager.set_budget(budget_data)
