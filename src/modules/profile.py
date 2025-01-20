
import uuid
import random
from src.modules.budget import Budget
from src.constants import default_income, default_categories

class Profile:
    """Represents a user profile with a budget."""
    
    def __init__(self, profile_id=None, name="Default Profile", income=default_income, budget=None):
        self.id = profile_id or str(uuid.uuid4())
        self.name = name
        self.income = income
        self.budget = budget or Budget(self.income)

    def get_category_color(self, category_name):
        """Retrieve the color associated with a category from the budget."""
        for category in self.budget.categories:
            if category.name == category_name:
                color = category.color
                if isinstance(color, str):  # Ensure it's a string
                    return color
                elif isinstance(color, float):  # Handle unexpected float values
                    print(f"WARNING: Found float instead of hex color for {category_name}. Using fallback.")
                    return random.choice([cat.color for cat in default_categories])
        
        fallback_color = random.choice([cat.color for cat in default_categories])
        return fallback_color
    
    def get_id(self):
        return self.id
    
    def get_budget(self):
        """Return the budget object."""
        return self.budget

    def to_dict(self):
        """Convert profile data to a dictionary for storage."""
        return {
            "profile_id": self.id,
            "profile_name": self.name,
            "income": self.income,
            "budget": self.budget.to_dict()
        }

    @staticmethod
    def from_dict(data):
        """Create a `Profile` instance from a dictionary."""
        return Profile(
            profile_id=data.get("profile_id", str(uuid.uuid4())),
            name=data.get("profile_name", "Default Profile"),
            income=data.get("income", 0.0),
            budget=Budget.from_dict(data.get("budget", {}))
        )