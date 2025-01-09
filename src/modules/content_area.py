from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from src.ui.views.dashboard_view import DashboardView
from src.ui.views.transaction_view import TransactionView

class DashboardScreen(Screen):
    pass

class TransactionScreen(Screen):
    pass

class ContentArea(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.transition = SlideTransition()
        self.add_widget(DashboardScreen(name="dashboard"))
        self.add_widget(TransactionScreen(name="transaction"))
        self.current = "dashboard"