import unittest
import os
import pandas as pd
from src.budget import Budget


class TestBudget(unittest.TestCase):
    def setUp(self):
        # Use a test path for the default budget
        self.test_budget_path = 'data/test_budget.csv'

        # Remove the file if it exists before running tests
        if os.path.exists(self.test_budget_path):
            os.remove(self.test_budget_path)

        # Initialize the Budget class to trigger default budget generation
        self.budget = Budget(self.test_budget_path)

    def tearDown(self):
        # Clean up the generated budget file
        if os.path.exists(self.test_budget_path):
            os.remove(self.test_budget_path)

    def test_default_budget_creation(self):
        # Verify the default budget file was created
        self.assertTrue(os.path.exists(self.test_budget_path))

    def test_total_expenses(self):
        # Verify the total expenses based on the default budget
        total = self.budget.get_total_expenses()
        self.assertEqual(total, 1500.00)  # Default budget total

    def test_income(self):
        # Verify the income based on the default budget
        income = self.budget.get_income()
        self.assertEqual(income, 2000.00)  # Default budget income

    def test_get_income_with_varied_formats(self):
        # Test different formats for Monthly Income
        varied_formats = [
            ('5300', 5300.00),  # No decimals
            ('5300.123', 5300.12),  # Too many decimals (should round)
            ('5300.', 5300.00),  # Not enough decimals
            ('$5,300.00', 5300.00),  # With $ and ,
            ('100000.00', 100000.00),  # Larger value
            ('$100,000.50', 100000.50)  # Larger value with $ and ,
        ]

        for input_value, expected_output in varied_formats:
            # Create a test budget file with the given format
            test_budget = {
                'Category': ['Income', 'Housing'],
                'Name': ['Monthly Income', 'Rent'],
                'Cost per Month': [input_value, '1800.00']
            }
            df = pd.DataFrame(test_budget)
            df.to_csv(self.test_budget_path, index=False)

            # Load the budget and assert income matches the expected output
            budget = Budget(self.test_budget_path)
            self.assertEqual(budget.get_income(), expected_output)

    def test_invalid_columns(self):
        # Test budget with incorrect columns
        invalid_budget = {
            'WrongColumn1': ['Income', 'Housing'],
            'WrongColumn2': ['Monthly Income', 'Rent'],
            'Cost': [2000.00, 1800.00]
        }
        df = pd.DataFrame(invalid_budget)
        df.to_csv(self.test_budget_path, index=False)

        with self.assertRaises(ValueError):
            Budget(self.test_budget_path)

if __name__ == '__main__':
    unittest.main()
