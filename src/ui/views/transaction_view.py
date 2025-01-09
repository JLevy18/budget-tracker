from kivy.uix.boxlayout import BoxLayout
from src.modules.classes.budget import Budget
from src.ui.views.budget_view import BudgetView
from kivy.clock import Clock

import os

budgets_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "budgets")
budgets_path = os.path.join(budgets_dir, "budget.csv")

class TransactionView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.initialize_widgets)
        
    def initialize_widgets(self, *args):
        self.add_budget_view("budget_view")
    def add_budget_view(self, widget_id):
        budget_view = BudgetView()
        
        budget = Budget(budgets_path)
        budget_view.budget = budget
        
        budget_view_area = self.ids[widget_id]
        budget_view_area.clear_widgets()
        budget_view_area.add_widget(budget_view)