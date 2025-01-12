from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from src.data_manager import get_data_manager


class BudgetView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
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
            self.add_colored_label(budget_info, category, row_color)
            self.add_colored_label(budget_info, name, row_color)
            self.add_colored_label(budget_info, f"${cost:.2f}", row_color)
            
    def add_colored_label(self, layout, text, background_color):
        """Add a single label with a background color."""
        label = Label(text=text, size_hint_y=None, height=30)
        with label.canvas.before:
            Color(*self.app.hex_to_rgba(background_color))
            Rectangle(size=label.size, pos=label.pos)
        label.bind(size=self.app.update_rect, pos=self.app.update_rect)
        layout.add_widget(label)