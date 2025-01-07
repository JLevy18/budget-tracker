from kivy.uix.boxlayout import BoxLayout
from src.modules.pie_chart import PieChart
from src.modules.bar_graph import BarGraph
from src.modules.radial_graph import RadialPercentageTracker
import matplotlib.pyplot as plt
import random

class DashboardView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Render pie charts in multiple widgets
        self.add_pie_chart("budget_category_pie_chart")
        self.add_pie_chart("actual_category_pie_chart")
        self.add_radial_tracker("radial_budget_progress", budget_percentage=30)
        self.add_bar_graph("monthly_spending_summary")

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
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        ax.set_facecolor("none")

        wedges, _ = ax.pie(data, labels=None, startangle=90, colors=colors)
        ax.axis("equal")

        # Assign data values to wedges
        for wedge, value in zip(wedges, data):
            wedge.data_value = value  # Assign data to the wedge

        pie_chart_widget = PieChart(fig)
        pie_chart_area = self.ids[widget_id]
        pie_chart_area.clear_widgets()
        pie_chart_area.add_widget(pie_chart_widget)

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




