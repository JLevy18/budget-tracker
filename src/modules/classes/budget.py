import pandas as pd
import os
import numbers
import logging


class Budget:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.budget_df = self.read_budget()

    def read_budget(self):
        if not os.path.exists(self.csv_path):
            logging.info("Budget file not found. Generating default budget.")
            self.generate_default_budget()
        
        try:
            df = pd.read_csv(self.csv_path)
            logging.info(f"Columns read from budget file: {df.columns.tolist()}")
        except Exception as e:
            logging.error(f"Failed to read budget file: {e}")
            raise
        
        # Ensure that the DataFrame has the expected columns
        expected_columns = ['Category', 'Name', 'Cost per Month']
        if list(df.columns) != expected_columns:
            logging.error(f"Expected columns {expected_columns}, but got {list(df.columns)}")
            raise ValueError(f"Expected columns {expected_columns}, but got {list(df.columns)}")

        # Clean the DataFrame by stripping whitespace from string columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip().fillna('')  # Fill NaN with empty strings for object columns

        # Ensure 'Cost per Month' is formatted with two decimals
        if 'Cost per Month' in df.columns:
            try:
                df['Cost per Month'] = (
                    df['Cost per Month']
                    .replace(r'[\$,]', '', regex=True)
                    .replace('', '0.0')  # Replace empty strings with '0.0'
                    .astype(float)
                    .round(2)
                )
            except ValueError as e:
                logging.error(f"Failed to convert 'Cost per Month' to float: {e}")
                raise

        return df

    def generate_default_budget(self):
        default_budget = {
            'Category': ['Income', 'Housing', 'Utilities', 'Insurance', 'Food & Essentials'],
            'Name': ['Monthly Income', 'Rent', 'Utilities', 'Auto', 'Groceries'],
            'Cost per Month': [2000.00, 1000.00, 100.00, 100.00, 300.00],
        }
        df = pd.DataFrame(default_budget)

        # Ensure the directory for the CSV exists
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)

        # Save the default budget as CSV
        try:
            df.to_csv(self.csv_path, index=False)
            logging.info(f"Default budget saved to {self.csv_path}")
        except Exception as e:
            logging.error(f"Failed to save default budget: {e}")
            raise

    def get_total_expenses(self):
        # Filter out the Income category and sum up expenses
        try:
            expenses = self.budget_df[self.budget_df['Category'] != 'Income']
            total = expenses['Cost per Month'].sum()
            logging.info(f"Total expenses calculated: {total}")
            return total
        except Exception as e:
            logging.error(f"Failed to calculate total expenses: {e}")
            raise

    def get_income(self):
        # Extract the income row
        try:
            income_row = self.budget_df[
                (self.budget_df['Category'] == 'Income') & 
                (self.budget_df['Name'] == 'Monthly Income')
            ]
            if not income_row.empty:
                income_val = income_row['Cost per Month'].values[0]
                logging.info(f"Income value extracted: {income_val}")
                return round(float(income_val), 2)
            else:
                logging.error("No Income category found in the budget.")
                raise ValueError("No Income category found in the budget.")
        except Exception as e:
            logging.error(f"Failed to get income: {e}")
            raise

    def display_budget(self):
        """
        Display the current budget in a readable format.
        """
        logging.info("Displaying the current budget.")
        print(self.budget_df)
