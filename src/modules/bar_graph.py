import matplotlib.pyplot as plt
import numpy as np
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from datetime import datetime

class BarGraph(FigureCanvasKivyAgg):

    def __init__(self, fig, ax, spending_data, **kwargs):
        """
        Initialize the bar graph.
        :param spending_data: List of monthly spending data (12 values, one for each month).
        """
        self.spending_data = spending_data
        self.current_year = datetime.now().year
        self.fig = fig
        self.ax = ax
        super().__init__(self.fig, **kwargs)

        self.create_bar_graph()

    def create_bar_graph(self):
        """Render the bar graph."""
        # Get the current month (or use the test month for simulation)
        current_month = datetime.now().month
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        # Determine the months to display (last 5 months + current month)
        if current_month < 6:  # Handle wrapping into the previous year
            previous_year_months = months[-(6 - current_month):]  # Get months from last year
            display_months = previous_year_months + months[:current_month]  # Combine last year and current year months
        else:
            display_months = months[current_month - 6:current_month]  # Get last 6 months

        # Slice the spending data to match the displayed months
        # Simulate data for the previous year (use the same spending data for simplicity)
        extended_spending_data = self.spending_data[-6:] + self.spending_data  # Add last 6 months of previous year
        display_spending = extended_spending_data[-6:]

        # Bar positions
        x_positions = np.arange(len(display_months))

        # Maximum spending for scaling
        max_spending = max(self.spending_data)
        y_limit = max_spending * 1.25  # Add 10% headroom to the top

        # Clear the plot
        self.ax.clear()

        # Create bars
        self.ax.bar(
            x_positions, display_spending, color="#116530", edgecolor="none"
        )

        # Set X-axis labels
        self.ax.set_xticks(x_positions)
        self.ax.set_xticklabels(display_months, fontsize=10, color="#FFFFFF")
        self.ax.tick_params(axis="x", length=0)

        step_candidates = [50, 100, 250, 500, 1000, 10000]  # Predefined step sizes
        step_size = next(s for s in step_candidates if max_spending / 6 <= s)  # Choose the smallest valid step
        y_limit = step_size * (max_spending // step_size + 1)  # Round up to the next step size multiple

        # Generate Y-axis ticks and labels
        y_ticks = np.arange(0, y_limit + step_size, step_size)  # Generate ticks
        y_labels = [f"${int(value)}" for value in y_ticks]
        y_labels[0] = ""  # Make the first label invisible
        y_labels[-1] = ""  # Make the last label invisible
        self.ax.set_yticks(y_ticks)  # Set only the ticks from the second value onward
        self.ax.set_yticklabels(y_labels, fontsize=8, color="#FFFFFF", va="center", x=0.03)
        

        # Customize the axes
        self.ax.spines["top"].set_visible(False)  # Remove top border
        self.ax.spines["right"].set_visible(False)  # Remove right border
        self.ax.spines["left"].set_visible(False)  # Remove left border
        self.ax.spines["bottom"].set_color("#FFFFFF")  # Keep bottom axis
        self.ax.spines["bottom"].set_linewidth(1)
        self.ax.tick_params(axis="y", length=0)  # Hide Y-axis ticks

        # Set graph title
        self.ax.set_title(
            f"{self.current_year} Monthly Spending",
            fontsize=14,
            color="#FFFFFF",
            pad=-20,
            weight="bold"
        )

        # Set Y-axis limit
        self.ax.set_ylim(0, y_limit)

        # Draw X-axis line
        self.ax.axhline(y=0, color="#FFFFFF", linewidth=1)

        # Finalize the figure
        self.fig.tight_layout()
        self.fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        self.draw_idle()

    def motion_notify_event(self, x, y, *args, **kwargs):
        pass
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