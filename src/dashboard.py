from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

# Ensure the KV file is loaded
import os

KV_DIR = os.path.join(os.path.dirname(__file__), "ui")
Builder.load_file(os.path.join(KV_DIR, "dashboard.kv"))


class DashboardScreen(BoxLayout):
    def __init__(self, budget, **kwargs):
        super().__init__(**kwargs)
        self.budget = budget
        self.display_budget()

    def display_budget(self):
        # Access the GridLayout with the ID "budget_info"
        budget_tab = self.ids["budget_info"]
        for _, row in self.budget.budget_df.iterrows():
            budget_tab.add_widget(Label(text=row["Category"]))
            budget_tab.add_widget(Label(text=row["Name"]))
            budget_tab.add_widget(Label(text=str(row["Cost per Month"])))


class BudgetTrackerApp(App):
    """
    The Kivy App class that launches the Dashboard.
    """
    def __init__(self, budget, **kwargs):
        super().__init__(**kwargs)
        self.budget = budget

    def build(self):
        # Create a DashboardScreen instance and return it as the root widget
        return DashboardScreen(budget=self.budget)
