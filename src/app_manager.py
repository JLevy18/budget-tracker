from src.budget import Budget
from src.modules.dashboard import BudgetTrackerApp
import os

def initialize_app(base_dir):
    """
    Initialize the application by ensuring directories exist and loading the budget.
    """
    # Path for the budgets directory and budget file
    budgets_dir = os.path.join(base_dir, "budgets")
    budget_path = os.path.join(budgets_dir, "budget.csv")

    # Ensure the budgets directory exists
    os.makedirs(budgets_dir, exist_ok=True)

    # Create the Budget instance
    budget = Budget(budget_path)

    return budget


def launch_dashboard(base_dir):
    """
    Launch the Kivy-based dashboard.
    """
    budget = initialize_app(base_dir)
    BudgetTrackerApp(budget).run()
