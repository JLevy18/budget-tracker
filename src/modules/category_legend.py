from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.app import App
from concurrent.futures import ThreadPoolExecutor
from src.modules.category import Category 
from src.data_manager import get_data_manager

class CategoryLegend(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(spacing=5, padding=[2, 2], **kwargs)
        self.app = App.get_running_app()
        self.active_profile = get_data_manager().get_active_profile()
        self.executor = ThreadPoolExecutor(max_workers=1)  # Limit to 1 worker
        self.size_hint_y = None  # Allow height adjustment
        self._update_scheduled = False  # Prevent duplicate updates
        self.bind(minimum_height=self.schedule_height_update)  # Throttle height updates
        get_data_manager().bind(on_profile_update=self.schedule_update)
        Clock.schedule_once(lambda dt: self.schedule_update())

    def schedule_height_update(self, *args):
        """Throttle height updates to prevent infinite loops."""
        if not self._update_scheduled:
            self._update_scheduled = True
            Clock.schedule_once(self.update_height, 0.05)  # Delay execution

    def update_height(self, *args):
        """Update height only if it has actually changed to prevent unnecessary updates."""
        self._update_scheduled = False  # Reset flag
        new_height = self.minimum_height
        if self.height != new_height:  # Prevent redundant updates
            self.height = new_height

    def schedule_update(self, *args):
        """Schedules background computation for updating categories."""
        self.executor.submit(self.compute_category_layout)

    def compute_category_layout(self):
        """Runs category layout calculations off the main thread and schedules UI updates."""
        budget = self.active_profile.get_budget()
        categories = budget.categories

        category_width = 150  # Approximate width of each category widget
        num_categories = len(categories)
        
        if num_categories == 0:
            Clock.schedule_once(lambda dt: self.update_ui([], 1))
            return

        total_spacing = self.spacing[0] * (num_categories - 1)
        available_width = self.width - self.padding[0] - self.padding[1] - total_spacing

        cols = max(1, int((available_width + self.spacing[0]) // (category_width + self.spacing[0])) - 1)

        category_data = []
        for category in categories:
            color = self.active_profile.get_category_color(category.name)
            if not isinstance(color, str):
                color = "#FFFFFF"
            rgba_color = self.app.hex_to_rgba(color)
            category_data.append((category.name, rgba_color))

        Clock.schedule_once(lambda dt: self.update_ui(category_data, cols))

    def update_ui(self, category_data, cols):
        """Updates UI elements on the main thread."""
        self.clear_widgets()
        self.cols = cols

        for name, rgba_color in category_data:
            category_widget = Category(name=name)
            category_widget.ids.color.color = rgba_color
            self.add_widget(category_widget)

        Clock.schedule_once(lambda dt: self.schedule_height_update())

    def on_size(self, *args):
        """Recalculate columns when resized."""
        self.schedule_update()