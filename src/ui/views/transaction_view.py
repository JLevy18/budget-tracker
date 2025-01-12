from kivy.uix.boxlayout import BoxLayout
from src.ui.views.budget_view import BudgetView
from kivy.clock import Clock

class TransactionView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.initialize_widgets)
        
    def initialize_widgets(self, dt):
        # Add the BudgetView widget
        self.add_budget_view("budget_view")

    def add_budget_view(self, widget_id):
        # Create the BudgetView and assign it directly
        budget_view = BudgetView()
        budget_view_area = self.ids[widget_id]
        budget_view_area.clear_widgets()
        budget_view_area.add_widget(budget_view)