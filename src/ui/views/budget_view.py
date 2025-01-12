from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from src.data_manager import get_data_manager


class BudgetView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_budget()

    def populate_budget(self):
        data_manager = get_data_manager()
        budget_data = data_manager.get_budget()

        budget_info = self.ids.budget_info
        budget_info.clear_widgets()
        for category, name, cost in zip(
            budget_data["Category"], budget_data["Name"], budget_data["Cost per Month"]
        ):
            budget_info.add_widget(Label(text=category))
            budget_info.add_widget(Label(text=name))
            budget_info.add_widget(Label(text=f"${cost:.2f}"))
