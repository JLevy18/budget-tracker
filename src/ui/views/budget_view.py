from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty


class BudgetView(BoxLayout):
    budget = ObjectProperty(None) 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(budget=self.on_budget_assigned)

    def on_budget_assigned(self, instance, value):
        """Called when the budget is set."""
        if value is not None:
            self.populate_budget(value)

    def populate_budget(self, budget):
        budget_info = self.ids.budget_info
        for _, row in budget.budget_df.iterrows():
            budget_info.add_widget(Label(text=row["Category"]))
            budget_info.add_widget(Label(text=row["Name"]))
            budget_info.add_widget(Label(text=str(row["Cost per Month"])))
