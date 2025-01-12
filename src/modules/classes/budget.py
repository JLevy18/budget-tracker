import pandas as pd
import os
import numbers
import logging


class Budget:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.budget_data = data_manager.get_budget()

    def get_total_expenses(self):
        try:
            expenses = self.budget_data["Cost per Month"]
            return round(sum(expenses), 2)
        except Exception as e:
            logging.error(f"Error calculating total expenses: {e}")
            raise

    def display_budget(self):
        """
        Display the current budget in a readable format.
        """
        logging.info("Displaying the current budget.")
        print("Category\tName\tCost per Month")
        for category, name, cost in zip(
            self.budget_data["Category"], self.budget_data["Name"], self.budget_data["Cost per Month"]
        ):
            print(f"{category}\t{name}\t{cost:.2f}")
