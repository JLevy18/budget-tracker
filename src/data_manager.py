import os
import pickle
import uuid
import logging

data_manager_instance = None

def set_data_manager(data_manager):
    global data_manager_instance
    data_manager_instance = data_manager

def get_data_manager():
    if data_manager_instance is None:
        raise ValueError("DataManager instance has not been initialized.")
    return data_manager_instance

class DataManager:
    def __init__(self, base_dir, is_prod):
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, "data")
        os.makedirs(self.data_dir, exist_ok=True)
        self.file_path = None
        self.active_profile = None

    def create_new_profile(self, profile_name=None, income=0.0):
        profile_name = profile_name or "Default Profile"
        profile_id = str(uuid.uuid4())
        file_path = os.path.join(self.data_dir, f"{profile_id}.dat")
        profile_data = {
            "profile_name": profile_name,
            "income": income,  # Default income
            "data": {
                "Category": ["Housing", "Utilities", "Insurance", "Food & Essentials"],
                "Name": ["Rent", "Utilities", "Auto", "Groceries"],
                "Cost per Month": [1000.00, 100.00, 100.00, 300.00],
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
                # Ensure required fields
                if "income" not in profile_data:
                    profile_data["income"] = 0.0
                if "data" not in profile_data:
                    profile_data["data"] = {
                        "Category": [],
                        "Name": [],
                        "Cost per Month": [],
                    }
                self.file_path = file_path
                self.active_profile = profile_data
                logging.info(f"Data loaded from {file_path}")
                return profile_data
        except Exception as e:
            logging.error(f"Failed to load data from {file_path}: {e}")
            raise

    def get_profiles(self):
        """
        Return a list of available profiles in the data directory.
        """
        profiles = []
        for file in os.listdir(self.data_dir):
            if file.endswith(".dat"):
                file_path = os.path.join(self.data_dir, file)
                try:
                    profile_data = self.load_data(file_path)
                    profiles.append({"name": profile_data["profile_name"], "path": file_path})
                except Exception:
                    logging.warning(f"Skipping corrupted or invalid file: {file}")
        return profiles

    def set_active_profile(self, file_path):
        """
        Set the active profile by loading the corresponding .dat file.
        """
        self.active_profile = self.load_data(file_path)

    def get_active_profile(self):
        if self.active_profile:
            return self.active_profile["data"]
        else:
            logging.error("No active profile set.")
            raise ValueError("No active profile set.")
    def get_income(self):
        if not self.active_profile:
            raise ValueError("No active profile loaded.")
        return self.active_profile.get("income", 0.0)

    def set_income(self, income):
        if not self.active_profile:
            raise ValueError("No active profile loaded.")
        self.active_profile["income"] = income
        self.save_data(self.file_path, self.active_profile)
        logging.info(f"Income updated to {income}")

    def get_budget(self):
        if not self.active_profile:
            raise ValueError("No active profile loaded.")
        return self.active_profile["data"]

    def set_budget(self, new_budget):
        if not self.active_profile:
            raise ValueError("No active profile loaded.")
        self.active_profile["data"] = new_budget
        self.save_data(self.file_path, self.active_profile)
        logging.info("Budget data updated.")
