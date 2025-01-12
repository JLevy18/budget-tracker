from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from src.data_manager import get_data_manager
from src.modules.pie_chart import PieChart
from src.modules.bar_graph import BarGraph
from src.modules.radial_graph import RadialPercentageTracker
from src.modules.classes.budget import Budget
from src.ui.views.budget_view import BudgetView
import matplotlib.pyplot as plt
import random
import os
import threading

budgets_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "budgets")
budgets_path = os.path.join(budgets_dir, "budget.csv")

class DashboardView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = get_data_manager()
        self.data_manager.bind(on_budget_change=self.on_budget_updated)
        Clock.schedule_once(self.initialize_widgets)

    def initialize_widgets(self, *args):
        # Safely access self.ids here
        self.add_pie_chart("budget_category_pie_chart")
        self.add_pie_chart("actual_category_pie_chart")
        self.add_radial_tracker("radial_budget_progress", budget_percentage=30)
        self.add_bar_graph("monthly_spending_summary")
        self.add_budget_view("budget_view")

    def on_budget_updated(self, *args):
        """
        Handle budget updates and refresh the pie charts.
        """
        threading.Thread(target=self.calculate_pie_chart_data, daemon=True).start()

    def calculate_pie_chart_data(self):
        """
        Perform pie chart calculations in a background thread.
        """
        # Perform data preparation asynchronously
        self.data_manager.assign_category_colors()
        budget_data = self.data_manager.get_budget()
        labels = budget_data["Category"]
        values = budget_data["Cost per Month"]
        percentages = self.data_manager.get_category_percentages()
        colors = [self.data_manager.get_category_color(category) for category in labels]

        # Schedule the rendering on the main thread
        Clock.schedule_once(lambda dt: self.render_pie_chart("budget_category_pie_chart", labels, values, percentages, colors))
        Clock.schedule_once(lambda dt: self.render_pie_chart("actual_category_pie_chart", labels, values, percentages, colors))

    def render_pie_chart(self, widget_id, labels, values, percentages, colors):
        """
        Render and update the pie chart on the main thread.
        """
        plt.close("all")

        # Create the Matplotlib figure
        fig, ax = plt.subplots(figsize=(5, 5))
        fig.patch.set_facecolor("none")
        fig.subplots_adjust(left=0, right=1, top=0.8, bottom=0)

        if widget_id == "budget_category_pie_chart":
            ax.set_title("Budgeted", fontsize=12, fontweight="bold", color="#FFFFFF", pad=10)
        elif widget_id == "actual_category_pie_chart":
            ax.set_title("Actual", fontsize=12, fontweight="bold", color="#FFFFFF", pad=10)
        ax.set_facecolor("none")

        wedges, _ = ax.pie(values, startangle=90, colors=colors)

        # Attach metadata to wedges
        for wedge, value, percentage in zip(wedges, values, percentages):
            wedge.data_value = value
            wedge.data_percentage = percentage

        pie_chart_widget = PieChart(fig)
        pie_chart_area = self.ids[widget_id]
        pie_chart_area.clear_widgets()
        pie_chart_area.add_widget(pie_chart_widget)

    def add_pie_chart(self, widget_id):
        pie_chart_area = self.ids[widget_id]
        pie_chart_area.bind(size=lambda instance, size: self.on_widget_ready(instance, size, widget_id))

    def on_widget_ready(self, instance, size, widget_id):
        if size[0] > 0 and size[1] > 0:  # Ensure size is valid
            threading.Thread(target=self.calculate_pie_chart_data, daemon=True).start()

    def add_radial_tracker(self, widget_id, budget_percentage):
        tracker_area = self.ids[widget_id]
    
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(5, 5))
        fig.patch.set_facecolor('none')  # Transparent figure background

        # Create the tracker widget
        tracker = RadialPercentageTracker(fig, ax, budget_percentage)
        # Add the tracker to the widget
        tracker_area.clear_widgets()
        tracker_area.add_widget(tracker)
    
    def add_bar_graph(self, widget_id):
        bar_graph_area = self.ids[widget_id]
        
        # Example spending data with last 3 months as 0
        monthly_spending = [500, 650, 700, 450, 800, 900, 1000, 850, 750, 0, 0, 0]

        # Create figure and axis
        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor('none')  # Transparent figure background
        ax.set_facecolor('none')

        # Create the bar graph widget
        bar_graph = BarGraph(spending_data=monthly_spending, fig=fig, ax=ax)

        # Add the bar graph to the widget
        bar_graph_area.clear_widgets()
        bar_graph_area.add_widget(bar_graph)
        
    def add_budget_view(self, widget_id):
        budget_view = BudgetView()

        budget_view_area = self.ids[widget_id]
        budget_view_area.clear_widgets()
        budget_view_area.add_widget(budget_view)

        



