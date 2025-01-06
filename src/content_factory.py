from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from matplotlib.patches import Wedge
import matplotlib.pyplot as plt
import numpy as np
import random
import random
import os
import math

KV_DIR = os.path.join(os.path.dirname(__file__), "ui", "views")  # Adjust to your folder structure
Builder.load_file(os.path.join(KV_DIR, "budget_view.kv"))
Builder.load_file(os.path.join(KV_DIR, "dashboard_view.kv"))

def is_point_in_wedge(point, wedge):
    """Manually check if a point is inside a wedge."""
    # Unpack point and wedge properties
    x, y = point
    center_x, center_y = wedge.center
    radius = wedge.r
    theta1, theta2 = wedge.theta1, wedge.theta2

    # Calculate distance from the center
    distance = ((x - center_x)**2 + (y - center_y)**2)**0.5
    if distance > radius:
        return False

    # Calculate angle in degrees
    angle = np.degrees(np.arctan2(y - center_y, x - center_x)) % 360

    # Normalize angles for comparison
    theta1 = theta1 % 360
    theta2 = theta2 % 360

    # Handle wrap-around cases
    if theta1 <= theta2:  # Normal case
        return theta1 <= angle <= theta2
    else:  # Wrapping case (e.g., 300° to 60°)
        return angle >= theta1 or angle <= theta2


class ContentFactory:
    def __init__(self, budget):
        self.budget = budget

    def create(self, page_name):
        if page_name == "dashboard":
            return self.create_dashboard_view()
        return None
    
    def create_dashboard_view(self):
        """Create the DashboardView and link BudgetView."""
        dashboard_view = DashboardView()

        # Create and add the BudgetView
        budget_view = BudgetView()
        budget_view.budget = self.budget
        dashboard_view.ids.budget_view.add_widget(budget_view)

        return dashboard_view

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

class SafeFigureCanvasKivyAgg(FigureCanvasKivyAgg):

    def __init__(self, fig, **kwargs):
        super().__init__(fig, **kwargs)
        self.fig = fig
        self.ax = fig.gca()
        self.hovered_section = None
        self.hover_text = None

        # Connect hover event
        self.fig.canvas.mpl_connect("motion_notify_event", self.motion_notify_event)

    def motion_notify_event(self, x, y, *args, **kwargs):
        """Handle mouse hover events."""
        # Convert Kivy's (x, y) into Matplotlib's figure coordinates
        data_coords = self.ax.transData.inverted().transform((x, y))
        if not self.ax.contains_point((x, y)):  # Ensure the event is within the plot axes
            self.clear_highlight()
            return
        for wedge in self.ax.patches:
            if is_point_in_wedge(data_coords, wedge):
                self.highlight_section(wedge)
                return
        self.clear_highlight()

    
    def highlight_section(self, wedge):
        """Enlarge the hovered section and display its value."""
        if self.hovered_section == wedge:
            return  # Already highlighted

        # Clear previous highlight
        self.clear_highlight()

        # Enlarge the hovered wedge
        if isinstance(wedge, Wedge):
            wedge.set_radius(1.1)  # Adjust as needed
        self.hovered_section = wedge

        # Display the value inside the wedge
        data_value = getattr(wedge, "data_value", "Unknown")
        theta_mid = (wedge.theta1 + wedge.theta2) / 2  # Middle angle of the wedge
        radius = wedge.r * 0.6  # Adjust the radius multiplier for better positioning

        # Convert polar to Cartesian coordinates
        x = radius * np.cos(np.radians(theta_mid))
        y = radius * np.sin(np.radians(theta_mid))

        # Add text at the calculated position
        if self.hover_text:
            self.hover_text.remove()
        self.hover_text = self.ax.text(
            x, y, f"{data_value}", ha="center", va="center", fontsize=12, color="black"
        )

        self.fig.canvas.draw_idle()

    def clear_highlight(self):
        """Reset the highlight and remove the hover text."""
        if self.hovered_section:
            self.hovered_section.set_radius(1.0)  # Reset radius
            self.hovered_section = None
        if self.hover_text:
            self.hover_text.remove()
            self.hover_text = None

        self.fig.canvas.draw_idle()
    def resize_event(self, *args, **kwargs):
        pass  
    def button_press_event(self, *args, **kwargs):
        pass
    def button_release_event(self, *args, **kwargs):
        pass  
    def key_press_event(self, *args, **kwargs):
        pass  
    def key_release_event(self, *args, **kwargs):
        pass
    def scroll_event(self, *args, **kwargs):
        pass  
class DashboardView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Render pie charts in multiple widgets
        self.add_pie_chart("budget_pie_chart")
        self.add_pie_chart("actual_pie_chart")

    def add_pie_chart(self, widget_id):
        pie_chart_area = self.ids[widget_id]

        # Wait until the widget has valid dimensions
        pie_chart_area.bind(size=lambda instance, size: self.on_widget_ready(instance, size, widget_id))

    def on_widget_ready(self, instance, size, widget_id):
        if size[0] > 0 and size[1] > 0:  # Ensure size is valid
            self.render_pie_chart(widget_id)

    def render_pie_chart(self, widget_id):
        labels = ["Category A", "Category B", "Category C", "Category D"]
        data = [random.randint(10, 100) for _ in labels]
        colors = ["#116530", "#21B6A8", "#A3EBB1", "#18A558"]

        fig, ax = plt.subplots(figsize=(5, 5))
        fig.patch.set_facecolor("none")
        ax.set_facecolor("none")

        wedges, _ = ax.pie(data, labels=None, startangle=90, colors=colors)
        ax.axis("equal")

        # Assign data values to wedges
        for wedge, value in zip(wedges, data):
            wedge.data_value = value  # Assign data to the wedge

        pie_chart_widget = SafeFigureCanvasKivyAgg(fig)
        pie_chart_area = self.ids[widget_id]
        pie_chart_area.clear_widgets()
        pie_chart_area.add_widget(pie_chart_widget)
