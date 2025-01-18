from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from src.ui.views.dashboard_view import DashboardView
from src.ui.views.transaction_view import TransactionView
from src.ui.views.settings_view import SettingsView
from src.ui.views.profile_view import ProfileView 

class DashboardScreen(Screen):
    pass

class TransactionScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class ContentArea(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.transition = SlideTransition()
        self.add_widget(DashboardScreen(name="dashboard"))
        self.add_widget(TransactionScreen(name="transaction"))
        self.add_widget(SettingsScreen(name="settings"))
        self.current = "dashboard"

class ProfileScreen(Screen):
    pass

class SettingsArea(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.transition = FadeTransition()
        self.add_widget(ProfileScreen(name="profile"))
        self.current = "profile"