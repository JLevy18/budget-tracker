import os
import pickle
import logging
import random
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty
from src.modules.profile import Profile
from src.modules.budget import Budget
from src.modules.configuration import Configuration

data_manager_instance = None

def set_data_manager(data_manager):
    global data_manager_instance
    data_manager_instance = data_manager

def get_data_manager():
    if data_manager_instance is None:
        raise ValueError("DataManager instance has not been initialized.")
    return data_manager_instance

class DataManager(EventDispatcher):
    _instance = None
    __events__ = ["on_profile_update"]
    
    budget_data = ObjectProperty()
    
    def __new__(cls, base_dir, is_prod):
        """Ensure only one instance of DataManager exists."""
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._instance.__init__(base_dir, is_prod)
        return cls._instance

    def __init__(self, base_dir, is_prod):
        self.category_colors = {}
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, "data")
        os.makedirs(self.data_dir, exist_ok=True)
        self.file_path = None
        
        self.config = Configuration(self.data_dir)
        self.active_profile = None
        

    def create_new_profile(self, profile_name=None, income=0.0):
        """Create a new profile with a default budget."""
        profile = Profile(name=profile_name or "Default Profile", income=income)
        file_path = os.path.join(self.data_dir, f"{profile.id}.dat")
        self.save_data(file_path, profile.to_dict())
        
        if self.config.get_default_profile() is None:
            self.config.set_default_profile(profile.id)
        
        logging.info(f"New profile '{profile.name}' created with ID: {profile.id}")
        return file_path

    def save_data(self, file_path, data):
        try:
            with open(file_path, "wb") as file:
                pickle.dump(data, file)
                logging.info(f"Data saved to {file_path}")
        except Exception as e:
            logging.error(f"Failed to save data to {file_path}: {e}")
            raise

    def load_data(self, file_path):
        """Load profile data from file and return a `Profile` instance."""
        try:
            with open(file_path, "rb") as file:
                profile_data = pickle.load(file)
                profile = Profile.from_dict(profile_data)
                logging.info(f"Data loaded from {file_path}")
                return profile
        except Exception as e:
            logging.error(f"Failed to load data from {file_path}: {e}")
            raise

    def load_profile(self, file_path):
        """
        Load the profile from a file and set it as active.
        """
        self.active_profile = self.load_data(file_path)

        if self.config.get_default_profile() is None:
            self.config.set_default_profile(self.active_profile.id)

    def get_profiles(self):
        """
        Return a list of available profiles in the data directory.
        """
        profiles = []
        for file in os.listdir(self.data_dir):
            file_path = os.path.join(self.data_dir, file)

            if file == Configuration.CONFIG_FILE or not file.endswith(".dat"):
                continue

            try:
                profile = self.load_data(file_path)
                profiles.append(profile)
            except Exception:
                logging.warning(f"Skipping corrupted or invalid file: {file}")

        return profiles

    def set_active_profile(self, file_path):
        """
        Set the active profile by loading the corresponding .dat file.
        """
        self.load_profile(file_path)

    def get_active_profile(self):
        """Return the active `Profile` instance instead of a dictionary."""
        if not self.active_profile:
            logging.error("No active profile set.")
            raise ValueError("No active profile set.")
        return self.active_profile
    
    def update_profile(self):
        """Save the entire active profile to its data file."""
        if not self.active_profile:
            raise ValueError("No active profile loaded.")

        file_path = os.path.join(self.data_dir, f"{self.active_profile.id}.dat")
        self.save_data(file_path, self.active_profile.to_dict())  # ✅ Save full profile

        self.dispatch("on_profile_update")
        logging.info(f"Profile '{self.active_profile.name}' updated and saved.")

    def on_profile_update(self, *args): pass