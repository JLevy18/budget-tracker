import tkinter as tk
from tkinter import ttk

class Dashboard:
    def __init__(self, root, budget_df):
        self.root = root
        self.root.title("Budget Tracker Dashboard")
        self.budget_df = budget_df

        # Create the table
        self.create_budget_table()

    def create_budget_table(self):
        # Create a Treeview widget to display the budget
        tree = ttk.Treeview(self.root, columns=("Category", "Name", "Cost per Month"), show="headings")
        tree.heading("Category", text="Category")
        tree.heading("Name", text="Name")
        tree.heading("Cost per Month", text="Cost per Month")

        # Populate the Treeview with budget data
        for _, row in self.budget_df.iterrows():
            tree.insert("", "end", values=(row["Category"], row["Name"], f"${row['Cost per Month']:.2f}"))

        # Pack the Treeview into the window
        tree.pack(expand=True, fill="both", padx=10, pady=10)


def launch_dashboard(budget):
    root = tk.Tk()
    app = Dashboard(root, budget.budget_df)
    root.mainloop()