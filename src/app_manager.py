import os
from src.budget import Budget

def initialize_app(base_dir):
    """
    Initialize the application by loading the budget.
    """
    # Path for the budget file
    budget_path = os.path.join(base_dir, "budgets", "budget.csv")

    # Create the Budget instance
    budget = Budget(budget_path)

    return budget