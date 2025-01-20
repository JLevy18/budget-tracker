from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from src.modules.editable_label import EditableLabel
from src.data_manager import get_data_manager
from src.ui.views.budget_view import BudgetView
from src.modules.category_legend import CategoryLegend
from kivy.clock import Clock

class ProfileView(BoxLayout):
    profile_name = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active_profile = get_data_manager().get_active_profile()
        self.profile_name = self.active_profile.name
        self.monthly_income = str(self.active_profile.income)
        Clock.schedule_once(self.initialize_widgets)
        
    def initialize_widgets(self, dt):
        pass
        # Add the BudgetView widget
        self.add_budget_view("budget_view")

    def add_budget_view(self, widget_id):
        # Create the BudgetView and assign it directly
        budget_view = BudgetView()
        budget_view_area = self.ids[widget_id]
        budget_view_area.clear_widgets()
        budget_view_area.add_widget(budget_view)
        
    def update_income(self, new_income):
        self.active_profile.income = float(new_income)
        get_data_manager().update_profile()
        self.monthly_income = float(new_income)

    def update_profile_name(self, new_name):
        """Update the profile name and save it."""
        self.active_profile.name = new_name
        get_data_manager().update_profile()
        self.profile_name = new_name