import os
import pickle
import uuid
import logging

class DataManager:
    def __init__(self, base_dir, is_prod):
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, "data")
        os.makedirs(self.data_dir, exist_ok=True)
        self.default_profile_name = "Default Profile"

        # Set the active profile (default or load existing later)
        self.active_profile = None

    def create_new_profile(self, profile_name=None):
        profile_name = profile_name or self.default_profile_name
        profile_id = str(uuid.uuid4())
        file_path = os.path.join(self.data_dir, f"{profile_id}.dat")
        profile_data = {
            "profile_name": profile_name,
            "data": {
                "Category": ["Income", "Housing", "Utilities", "Insurance", "Food & Essentials"],
                "Name": ["Monthly Income", "Rent", "Utilities", "Auto", "Groceries"],
                "Cost per Month": [2000.00, 1000.00, 100.00, 100.00, 300.00],
            }
        }
        self.save_data(file_path, profile_data)
        logging.info(f"New profile '{profile_name}' created with ID: {profile_id}")
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
        try:
            with open(file_path, "rb") as file:
                profile_data = pickle.load(file)
                logging.info(f"Data loaded from {file_path}")
                return profile_data
        except Exception as e:
            logging.error(f"Failed to load data from {file_path}: {e}")
            raise

    def get_profiles(self):
        """
        Return a list of all available profiles in the data directory.
        """
        profiles = []
        for file in os.listdir(self.data_dir):
            if file.endswith(".dat"):
                try:
                    profile_data = self.load_data(os.path.join(self.data_dir, file))
                    profiles.append({"name": profile_data["profile_name"], "path": os.path.join(self.data_dir, file)})
                except Exception:
                    logging.warning(f"Skipping corrupted or invalid file: {file}")
        return profiles

    def set_active_profile(self, file_path):
        """
        Set the active profile by loading the corresponding .dat file.
        """
        self.active_profile = self.load_data(file_path)

    def get_active_data(self):
        if self.active_profile:
            return self.active_profile["data"]
        else:
            logging.error("No active profile set.")
            raise ValueError("No active profile set.")
