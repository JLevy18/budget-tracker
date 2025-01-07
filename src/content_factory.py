from kivy.uix.label import Label
from kivy.lang import Builder

from src.modules.classes.budget import Budget
from src.ui.views.dashboard_view import DashboardView
from src.ui.views.budget_view import BudgetView

import os
import math

KV_DIR = os.path.join(os.path.dirname(__file__), "ui", "views")  # Adjust to your folder structure
Builder.load_file(os.path.join(KV_DIR, "budget_view.kv"))
Builder.load_file(os.path.join(KV_DIR, "dashboard_view.kv"))

class ContentFactory:

    budgets_dir = os.path.join(os.path.dirname(__file__), "data", "budgets")
    budgets_path = os.path.join(budgets_dir, "budget.csv")

    def create(self, page_name):
        if page_name == "dashboard":
            return self.create_dashboard_view()
        return None
    
    def create_dashboard_view(self):
        """Create the DashboardView and link BudgetView."""
        dashboard_view = DashboardView()

        # Create and add the BudgetView
        budget_view = BudgetView()
        budget_view.budget = Budget(self.budgets_path)
        dashboard_view.ids.budget_view.add_widget(budget_view)

        return dashboard_view
  

