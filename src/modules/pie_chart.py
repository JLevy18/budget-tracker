from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from matplotlib.patches import Wedge

import numpy as np

class PieChart(FigureCanvasKivyAgg):

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
        total_data = sum([w.data_value for w in self.ax.patches if hasattr(w, "data_value")])
        percentage = (wedge.data_value / total_data) * 100 if total_data > 0 else 0
        theta_mid = (wedge.theta1 + wedge.theta2) / 2  # Middle angle of the wedge
        radius = wedge.r * 0.6  # Adjust the radius multiplier for better positioning

        # Convert polar to Cartesian coordinates
        x = radius * np.cos(np.radians(theta_mid))
        y = radius * np.sin(np.radians(theta_mid))

        # Add text at the calculated position
        if self.hover_text:
            self.hover_text.remove()
        self.hover_text = self.ax.text(
            x, y, f"{percentage:.1f}%", ha="center", va="center", fontsize=10, color="black"
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