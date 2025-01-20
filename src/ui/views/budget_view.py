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
        self.active_profile = get_data_manager().get_active_profile()
        self.populate_budget()
    
    def populate_budget(self):
        """Populate the budget view with data from the active profile."""
        budget = self.active_profile.get_budget() 

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
        i = 0
        for category in budget.categories:
            active_expenses = [expense for expense in category.expenses if expense.name in budget.names]

            for expense in active_expenses:
                expense_name = expense.name  # 🔥 Extract name from named tuple

                row_color = row_colors[i % len(row_colors)]
                cost_index = budget.names.index(expense_name) if expense_name in budget.names else -1
                cost_value = budget.costs[cost_index] if cost_index >= 0 else 0.0

                self.add_editable_cell(budget_info, category.name, i, "Category", row_color)
                self.add_editable_cell(budget_info, expense_name, i, "Name", row_color)
                self.add_editable_cell(budget_info, f"${cost_value:.2f}", i, "Cost per Month", row_color)

                i += 1
    
            
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
        """Update the budget data in the active profile and save it."""
        budget = self.active_profile.get_budget()

        if column_name == "Category":
            budget.categories[row_index] = new_text
        elif column_name == "Name":
            budget.names[row_index] = new_text
        elif column_name == "Cost per Month":
            try:
                clean_value = new_text.replace("$", "").replace(",", "")
                budget.costs[row_index] = round(float(clean_value), 2)
            except ValueError:
                pass  # Ignore invalid input
        
        self.active_profile.budget = budget
        get_data_manager().update_profile()