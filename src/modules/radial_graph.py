from matplotlib.patches import Wedge, Circle
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import calendar
import time



class RadialPercentageTracker(FigureCanvasKivyAgg):
    def __init__(self, fig, ax, budget_percentage, **kwargs):
        super().__init__(fig, **kwargs)
        self.ax = ax
        self.fig = fig
        self.budget_percentage = budget_percentage

        self.create_radial_graph()
    
    def create_radial_graph(self):
        """Render the radial graph."""
        # Clear existing axis content
        self.ax.clear()
        self.ax.set_xlim(-1.5, 1.5)
        self.ax.set_ylim(-1.5, 1.5)
        self.ax.set_aspect('equal')
        self.ax.set_facecolor('none')


        now = datetime.now()
        current_day = now.day
        current_month = now.month
        current_year = now.year
        total_days = calendar.monthrange(current_year, current_month)[1]

        # Calculate the end angle based on the percentage
        start_angle = 90  # Start at 12 o'clock
        end_angle = start_angle + 360 * ((100 - self.budget_percentage) / 100)

        # Create the progress wedge (filled area)
        progress_wedge = Wedge(
            center=(0, 0),
            r=1,
            theta1=end_angle, 
            theta2=start_angle,  # Clockwise fill
            width=0.25, 
            facecolor="#116530",  # Green progress
            edgecolor="none", 
            antialiased=True
        )
        self.ax.add_patch(progress_wedge)

        # Add tick marks for each day of the month
        tick_outer_multiplier = 1.2  # Move ticks farther out from the wedge
        tick_inner_multiplier = 1.15  # Set the inner tick point closer than the outer
        tick_length = 0.1  # Length of the tick marks
        tick_thickness = 1.2  # Thickness of the tick marks
        text_padding = 0.2

        def get_day_suffix(day):
            """Return the suffix for the day (e.g., 'st', 'nd', 'rd', 'th')."""
            if 11 <= day <= 13:
                return "th"
            elif day % 10 == 1:
                return "st"
            elif day % 10 == 2:
                return "nd"
            elif day % 10 == 3:
                return "rd"
            else:
                return "th"

        for day_offset in range(total_days):
            day = (total_days - day_offset)  # Start with the last day at the top
            angle = start_angle + (360 / total_days) * day_offset  # Clockwise tick angle
            x_outer = tick_outer_multiplier * np.cos(np.radians(angle))  # Outer tick mark position
            y_outer = tick_outer_multiplier * np.sin(np.radians(angle))
            x_inner = (tick_outer_multiplier - tick_length) * np.cos(np.radians(angle))  # Extend inner tick to make it longer
            y_inner = (tick_outer_multiplier - tick_length) * np.sin(np.radians(angle))
            self.ax.plot([x_outer, x_inner], [y_outer, y_inner], color="#FFFFFF", linewidth=tick_thickness)

            # Add day numbers at every 5th tick for clarity
            if day == total_days or day == current_day:
                suffix = get_day_suffix(day)
                day_label = f"{day}"
                x_label = (tick_outer_multiplier + text_padding) * np.cos(np.radians(angle))  # Position the label slightly further out
                y_label = (tick_outer_multiplier + text_padding) * np.sin(np.radians(angle))
                self.ax.text(
                    x_label, y_label, f"{day_label}",
                    ha='center', va='center', fontsize=10, fontweight="semibold", color="#FFFFFF"
                )

                # Add suffix relative to the day label
                if 45 < angle <= 135:  # Top side
                    suffix_x = x_label + 0.13
                    suffix_y = y_label + 0.05
                else:  # Left side
                    suffix_x = x_label + 0.15
                    suffix_y = y_label + 0.05

                self.ax.text(
                    suffix_x, suffix_y, suffix,
                    ha='center', va='center', fontsize=8, fontweight="light", color="#FFFFFF"
                )


        # Add percentage text in the center
        self.ax.text(
            0, 0.1, f"{self.budget_percentage}%", 
            ha='center', va='center', fontsize=16, color="#FFFFFF", fontweight='bold'
        )

        self.ax.text(
            0, -0.15, "Spent so far",  # Slightly below the center
            ha='center', 
            va='center', 
            fontsize=10,  # Smaller font size for the label
            color="#FFFFFF", 
            fontweight='normal'  # Lighter weight for the text
        )

        # Hide axes
        self.ax.axis('off')
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0.05)
        # Redraw the figure
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