import pandas as pd
import os
import numbers
import logging
from src.constants import default_categories

class Budget:
    """Encapsulates budget data and operations."""
    def __init__(self, income, is_home_owner=False, is_vehicle_owner=True, categories=None, names=None, costs=None, custom_weights=None):
        self.income = income
        self.is_home_owner = is_home_owner
        self.is_vehicle_owner = is_vehicle_owner
        self.categories = categories or default_categories
        self.names = names if names else []
        self.costs = costs if costs else []
        
        self.budget_weights = custom_weights or {cat.name: cat.weight for cat in self.categories}
        
        if not self.names:
            self.assemble_budget()

    def assemble_budget(self):
        """Dynamically allocate budget based on income and category weights."""
        total_income = self.income
        allocated_budget = {cat.name: round(total_income * cat.weight, 2) for cat in self.categories}

        logging.debug(f"Allocated budget per category: {allocated_budget}")

        self.names, self.costs = [], []

        for category in self.categories:
            allocated_amount = allocated_budget[category.name]
            selected_expenses = []

            if category.name == "Housing & Utilities":
                if self.is_home_owner:
                    selected_expenses.append(("Mortgage", 0.5))
                    selected_expenses.append(("Property Taxes", 0.2))
                    selected_expenses.append(("Homeowners Insurance", 0.1))
                    selected_expenses.append(("Home Maintenance & Repairs", 0.2))
                else:
                    selected_expenses.append(("Rent", 0.7))
                    selected_expenses.append(("Renter’s Insurance", 0.1))

                # Everyone Pays Utilities
                selected_expenses.append(("Electricity", 0.05))
                selected_expenses.append(("Internet", 0.05))
                selected_expenses.append(("Cell Phone", 0.05))

            elif category.name == "Transportation":
                if self.is_vehicle_owner:
                    selected_expenses.append(("Car Payment", 0.5))
                    selected_expenses.append(("Car Insurance", 0.2))
                    selected_expenses.append(("Gas", 0.3))
                else:
                    selected_expenses.append(("Public Transportation", 0.8))
                    selected_expenses.append(("Ride-Sharing", 0.2))

            elif category.name == "Debt & Financial Obligations":
                selected_expenses.append(("Student Loan Payments", 1.0))

            elif category.name == "Savings & Investments":
                selected_expenses.append(("Emergency Fund", 0.5))
                selected_expenses.append(("Retirement Contributions", 0.5))

            elif category.name == "Shopping & Miscellaneous":
                selected_expenses.append(("Clothing", 0.4))
                selected_expenses.append(("Shoes", 0.2))
                selected_expenses.append(("Beauty & Cosmetics", 0.2))
                selected_expenses.append(("Tech & Gadgets", 0.2))

            for expense_name, weight in selected_expenses:
                self.names.append(expense_name)
                self.costs.append(round(allocated_amount * weight, 2))


    def get_total(self):
        """Calculate total budget."""
        return sum(self.costs)

    def get_category_percentages(self):
        """Calculate category percentage breakdown."""
        total = self.get_total()
        return [(cost / total) * 100 if total > 0 else 0 for cost in self.costs]

    def to_dict(self):
        """Convert budget data to a dictionary for storage."""
        return {
            "income": self.income,
            "categories": self.categories,
            "names": self.names,
            "costs": self.costs,
            "budget_weights": self.budget_weights
        }

    @staticmethod
    def from_dict(data):
        """Create a `Budget` instance from a dictionary."""
        return Budget(
            income=data.get("income", []),
            categories=data.get("categories", []),
            names=data.get("names", []),
            costs=data.get("costs", []),
            custom_weights=data.get("budget_weights", [])
        )