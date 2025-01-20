from kivy.uix.boxlayout import BoxLayout
from src.data_manager import get_data_manager

class SettingsView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from src.modules.content_area import SettingsArea
        self.settings_area = SettingsArea()
        self.active_profile = get_data_manager().get_active_profile().id

    def switch_screen(self, screen_name):
        """Switch to the specified screen."""
        sm = self.ids.settings_area

        # Switch screens only if the target screen is different
        if sm.current != screen_name:
            sm.current = screen_name